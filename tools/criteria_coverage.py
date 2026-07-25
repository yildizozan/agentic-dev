#!/usr/bin/env python3
"""Criteria coverage checker — docs/02-spec-fidelity.md §2.1 altın kuralını uygular.

Her AC-### için görünür test suite'inde VEYA gizli set manifest'inde o ID'ye
referans veren en az bir test bulunmak zorundadır.

v1.0'daki çelişkinin çözümü: gizli set testlerin İÇERİĞİNİ değil yalnız AC ID
listesini yayınlar (tests/hidden/manifest.txt). Böylece kapsama ölçülebilir,
test içeriği ajandan gizli kalır.

Kullanım:
    python3 tools/criteria_coverage.py
    python3 tools/criteria_coverage.py --format markdown --out report.md
    python3 tools/criteria_coverage.py --strict     # uyarıları da hata say

Çıkış kodları:
    0  geçti
    1  ihlal var (öksüz AC, öksüz test, onaysız AC, ...)
    2  konfigürasyon/kullanım hatası
Bağımlılık: yok (yalnız stdlib).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

AC_ID = re.compile(r"\bAC-(\d{3,})\b")
FRONTMATTER_KV = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")

# Fixture/ornek AC ID'si iceren dosyalar bu isareti tasir (meta-testler, sablonlar).
# GUVENLI: isaret yalnizca referans KALDIRIR, kapsama URETEMEZ. Kotuye kullanimi
# build'i kirmizilastirir, yesillestirmez -> gate'i atlatmak icin kullanilamaz.
IGNORE_MARKER = "criteria-coverage:ignore-file"

DEFAULT_SPEC_DIR = "specs/acceptance-criteria"
DEFAULT_HIDDEN_MANIFEST = "tests/hidden/manifest.txt"
DEFAULT_TEST_GLOBS = [
    "tests/**/*",
    "test/**/*",
    "src/**/*_test.*",
    "src/**/*.test.*",
    "src/**/*.spec.*",
    "**/*Tests.cs",
    "**/*Test.kt",
    "**/*_test.go",
]
# Gizli test İÇERİĞİ hiçbir zaman taranmaz — yalnız manifest okunur.
EXCLUDE_DIRS = {".git", "node_modules", "build", "dist", ".dart_tool",
                "Library", "obj", "bin", "__pycache__", "vendor",
                "tests/hidden", "test/hidden"}
TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".dart", ".cs", ".kt", ".kts",
    ".java", ".go", ".rb", ".rs", ".swift", ".m", ".mm", ".php",
    ".feature", ".yaml", ".yml", ".json", ".sql", ".sh", ".md",
    ".txt", ".tags",   # .tags = kapsama beyan dosyalari (bkz. IGNORE_MARKER notu)
}


@dataclass
class Criterion:
    ac_id: str
    path: Path
    title: str = ""
    hidden: bool = False
    approved: bool = False
    approved_by: str = ""
    status: str = "active"
    version: str = "1"


@dataclass
class Report:
    criteria: dict[str, Criterion] = field(default_factory=dict)
    visible_refs: dict[str, set[Path]] = field(default_factory=dict)
    hidden_ids: set[str] = field(default_factory=set)
    ignored_files: list[Path] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = FRONTMATTER_KV.match(line.strip())
        if m:
            out[m.group(1).lower()] = m.group(2).strip().strip("\"'")
    return out


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1", "evet"}


def load_criteria(spec_dir: Path, rep: Report) -> None:
    if not spec_dir.is_dir():
        rep.errors.append(
            f"AC dizini bulunamadi: {spec_dir} "
            f"(templates/acceptance-criteria.md sablonunu kullan)"
        )
        return

    for path in sorted(spec_dir.rglob("*.md")):
        if path.name.upper().startswith("README"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)

        ac_id = fm.get("id", "").strip()
        if not ac_id:
            m = AC_ID.search(path.stem) or AC_ID.search(text)
            ac_id = m.group(0) if m else ""
        if not ac_id:
            rep.errors.append(f"{path}: AC ID bulunamadi (frontmatter `id:` gerekli)")
            continue
        if not AC_ID.fullmatch(ac_id):
            rep.errors.append(f"{path}: gecersiz AC ID formati: {ac_id!r} (AC-### bekleniyor)")
            continue
        if ac_id in rep.criteria:
            rep.errors.append(f"{path}: {ac_id} zaten tanimli ({rep.criteria[ac_id].path})")
            continue

        rep.criteria[ac_id] = Criterion(
            ac_id=ac_id,
            path=path,
            title=fm.get("title", ""),
            hidden=truthy(fm.get("hidden", "false")),
            approved=truthy(fm.get("approved", "false")),
            approved_by=fm.get("approved_by", ""),
            status=fm.get("status", "active").lower(),
            version=fm.get("version", "1"),
        )


def is_excluded(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix()
    parts = set(rel.split("/"))
    if parts & EXCLUDE_DIRS:
        return True
    return any(rel.startswith(d + "/") or rel == d for d in EXCLUDE_DIRS)


def scan_visible_tests(root: Path, globs: list[str], rep: Report) -> None:
    seen: set[Path] = set()
    for pattern in globs:
        for path in root.glob(pattern):
            if not path.is_file() or path in seen:
                continue
            if is_excluded(path, root):
                continue
            if path.suffix and path.suffix not in TEXT_SUFFIXES:
                continue
            seen.add(path)
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if IGNORE_MARKER in text:
                rep.ignored_files.append(path)
                continue
            for m in AC_ID.finditer(text):
                rep.visible_refs.setdefault(m.group(0), set()).add(path)


def load_hidden_manifest(manifest: Path, rep: Report) -> None:
    """Gizli set manifest'i: satir basina bir AC ID. Test icerigi ASLA burada olmaz."""
    if not manifest.is_file():
        rep.warnings.append(
            f"Gizli set manifest'i yok: {manifest} — gizli set kurulmadiysa normal "
            f"(docs/02-spec-fidelity.md §4.3)"
        )
        return
    for lineno, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if not AC_ID.fullmatch(line):
            rep.errors.append(
                f"{manifest}:{lineno}: yalnizca AC-### satirlari olabilir, bulunan: {line!r}. "
                f"Manifest'e test icerigi/dosya adi yazilamaz."
            )
            continue
        rep.hidden_ids.add(line)


def evaluate(rep: Report) -> None:
    active = {i: c for i, c in rep.criteria.items() if c.status == "active"}

    # 1. Oksuz AC — ne gorunur ne gizli testi var
    for ac_id, crit in sorted(active.items()):
        has_visible = ac_id in rep.visible_refs
        has_hidden = ac_id in rep.hidden_ids
        if not has_visible and not has_hidden:
            rep.errors.append(
                f"{ac_id} TESTSIZ ({crit.path}) — gorunur suite'te referans yok, "
                f"gizli manifest'te de yok. docs/02 §2.1 altin kurali."
            )
        if crit.hidden and not has_hidden:
            rep.warnings.append(
                f"{ac_id} `hidden: true` isaretli ama gizli manifest'te yok — "
                f"gizli test yazilmamis olabilir."
            )

    # 2. Insan onayi olmayan aktif AC — docs/05 §3.2 G1
    for ac_id, crit in sorted(active.items()):
        if not crit.approved:
            rep.errors.append(
                f"{ac_id} INSAN ONAYI YOK ({crit.path}) — `approved: true` + `approved_by:` "
                f"gerekli. docs/05 §3.2 G1: zincirdeki tek ground truth."
            )
        elif not crit.approved_by.strip():
            rep.errors.append(f"{ac_id}: `approved: true` ama `approved_by` bos ({crit.path})")

    # 3. Oksuz test referansi — var olmayan AC'ye atif
    for ac_id, paths in sorted(rep.visible_refs.items()):
        if ac_id not in rep.criteria:
            where = ", ".join(sorted(str(p) for p in list(paths)[:3]))
            rep.errors.append(
                f"{ac_id} testlerde referans veriliyor ama boyle bir AC yok ({where})"
            )

    # 4. Superseded AC'ye hala referans — docs/06 §4
    for ac_id, crit in sorted(rep.criteria.items()):
        if crit.status == "superseded" and ac_id in rep.visible_refs:
            where = ", ".join(sorted(str(p) for p in list(rep.visible_refs[ac_id])[:3]))
            rep.warnings.append(
                f"{ac_id} `status: superseded` ama testler hala referans veriyor ({where}) — "
                f"spec degisim protokolu tamamlanmamis (docs/06 §4)"
            )

    # 5. Gizli manifest'te olan ama AC dosyasi olmayan
    for ac_id in sorted(rep.hidden_ids - set(rep.criteria)):
        rep.errors.append(f"{ac_id} gizli manifest'te ama AC dosyasi yok")


def coverage_pct(rep: Report) -> tuple[int, int, float]:
    active = [c for c in rep.criteria.values() if c.status == "active"]
    covered = sum(
        1 for c in active if c.ac_id in rep.visible_refs or c.ac_id in rep.hidden_ids
    )
    pct = (covered / len(active) * 100) if active else 100.0
    return covered, len(active), pct


def render_text(rep: Report) -> str:
    covered, total, pct = coverage_pct(rep)
    out = [
        "Criteria Coverage",
        "=" * 40,
        f"Aktif AC        : {total}",
        f"Testli          : {covered}",
        f"Kriter kapsamasi: {pct:.1f}%   (hedef 100%)",
        f"  gorunur test  : {len([i for i in rep.visible_refs if i in rep.criteria])}",
        f"  gizli manifest: {len(rep.hidden_ids)}",
    ]
    if rep.ignored_files:
        out.append(f"Taranmayan dosya: {len(rep.ignored_files)} ({IGNORE_MARKER})")
        out += [f"  - {p}" for p in rep.ignored_files]
    out.append("")
    if rep.errors:
        out.append(f"HATA ({len(rep.errors)}):")
        out += [f"  x {e}" for e in rep.errors]
        out.append("")
    if rep.warnings:
        out.append(f"UYARI ({len(rep.warnings)}):")
        out += [f"  ! {w}" for w in rep.warnings]
        out.append("")
    out.append("GECTI" if not rep.errors else "BASARISIZ")
    return "\n".join(out)


def render_markdown(rep: Report) -> str:
    covered, total, pct = coverage_pct(rep)
    icon = "✅" if not rep.errors else "❌"
    out = [
        f"## {icon} Criteria Coverage — {pct:.1f}%",
        "",
        "| | |",
        "|---|---|",
        f"| Aktif AC | {total} |",
        f"| Testli | {covered} |",
        f"| Görünür testle | {len([i for i in rep.visible_refs if i in rep.criteria])} |",
        f"| Gizli manifestle | {len(rep.hidden_ids)} |",
        f"| Hedef | 100% |",
        f"| Taranmayan dosya | {len(rep.ignored_files)} |",
        "",
    ]
    if rep.errors:
        out += [f"### ❌ Hata ({len(rep.errors)})", ""]
        out += [f"- {e}" for e in rep.errors] + [""]
    if rep.warnings:
        out += [f"### ⚠️ Uyarı ({len(rep.warnings)})", ""]
        out += [f"- {w}" for w in rep.warnings] + [""]
    if not rep.errors and not rep.warnings:
        out.append("Tüm aktif kabul kriterlerinin testi ve insan onayı var.")
    out += ["", "<sub>`tools/criteria_coverage.py` · kural: `docs/02-spec-fidelity.md` §2.1</sub>"]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="AC -> test kriter kapsamasi kontrolu")
    ap.add_argument("--root", default=".", help="repo koku")
    ap.add_argument("--spec-dir", default=DEFAULT_SPEC_DIR)
    ap.add_argument("--hidden-manifest", default=DEFAULT_HIDDEN_MANIFEST)
    ap.add_argument("--test-glob", action="append", default=None,
                    help="tekrarlanabilir; varsayilanlari degistirir")
    ap.add_argument("--format", choices=["text", "markdown"], default="text")
    ap.add_argument("--out", help="raporu dosyaya da yaz (PR yorumu icin)")
    ap.add_argument("--strict", action="store_true", help="uyarilari da hata say")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"repo koku yok: {root}", file=sys.stderr)
        return 2

    rep = Report()
    load_criteria(root / args.spec_dir, rep)
    scan_visible_tests(root, args.test_glob or DEFAULT_TEST_GLOBS, rep)
    load_hidden_manifest(root / args.hidden_manifest, rep)
    evaluate(rep)

    text = render_markdown(rep) if args.format == "markdown" else render_text(rep)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")

    if rep.errors:
        return 1
    if args.strict and rep.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
