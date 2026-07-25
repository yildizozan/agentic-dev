"""Acceptance testleri — AC-001: Repo kurallarının çalıştırılabilir olduğu doğrulanır.

Sahibi: agent:qa. Engineer ajanı bu dosyaya YAZAMAZ (docs/02-spec-fidelity.md §4.1-4.2).

Bağımlılık yok: `python3 tests/acceptance/test_criteria_coverage.py` ile doğrudan koşar
(pytest ile de koşar).

criteria-coverage:ignore-file
    Bu dosya fixture olarak sahte AC ID'leri (AC-101..AC-108, AC-999) üretir.
    İşaret olmadan checker onları gerçek referans/öksüz referans sanar.
    İşaret yalnız referans kaldırır, kapsama üretemez — gate atlatmak için
    kullanılamaz (tools/criteria_coverage.py IGNORE_MARKER).
    AC-001 kapsaması bu dosya yerine tests/acceptance/AC-001.tags ile beyan edilir.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import criteria_coverage as cc  # noqa: E402

AC_TEMPLATE = """---
id: {ac_id}
title: test fixture
version: 1
status: {status}
hidden: {hidden}
approved: {approved}
approved_by: {approved_by}
---
# {ac_id}
"""


def build_repo(root: Path, acs, test_body="", hidden_manifest=None):
    spec_dir = root / "specs/acceptance-criteria"
    spec_dir.mkdir(parents=True, exist_ok=True)
    for ac in acs:
        (spec_dir / f"{ac['ac_id']}.md").write_text(
            AC_TEMPLATE.format(
                ac_id=ac["ac_id"],
                status=ac.get("status", "active"),
                hidden=str(ac.get("hidden", False)).lower(),
                approved=str(ac.get("approved", True)).lower(),
                approved_by=ac.get("approved_by", "human"),
            ),
            encoding="utf-8",
        )
    tests = root / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "sample_test.py").write_text(test_body or "# no refs\n", encoding="utf-8")
    if hidden_manifest is not None:
        hidden = root / "tests/hidden"
        hidden.mkdir(parents=True, exist_ok=True)
        (hidden / "manifest.txt").write_text(hidden_manifest, encoding="utf-8")


def run(root: Path) -> int:
    return cc.main(["--root", str(root), "--format", "text"])


# ── AC-001 · Scenario: Testli ve onaylı AC geçer ───────────────────────────────
def test_ac001_approved_and_tested_passes():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(root, [{"ac_id": "AC-101"}], test_body="def test_x(): # AC-101\n    pass\n")
        assert run(root) == 0, "onaylı + testli AC gecmeliydi"


# ── AC-001 · Scenario: Testsiz AC build'i kırar ────────────────────────────────
def test_ac001_untested_ac_fails():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(root, [{"ac_id": "AC-102"}], test_body="# hicbir referans yok\n")
        assert run(root) == 1, "testsiz AC build'i kirmaliydi"


# ── AC-001 · Scenario: Gizli manifest kapsama sayılır ─────────────────────────
def test_ac001_hidden_manifest_counts_as_coverage():
    """docs/02 §2.1: v1.0'daki 'altın kural ↔ gizli set' çelişkisinin regresyon testi."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(
            root,
            [{"ac_id": "AC-103", "hidden": True}],
            test_body="# gorunur suite'te referans YOK\n",
            hidden_manifest="# yalniz AC ID'leri\nAC-103\n",
        )
        assert run(root) == 0, "gizli manifest'teki AC testli sayilmaliydi"


# ── AC-001 · Negatif: İnsan onayı olmayan AC reddedilir ───────────────────────
def test_ac001_unapproved_ac_rejected():
    """docs/05 §3.2 G1: zincirdeki tek ground truth."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(
            root,
            [{"ac_id": "AC-104", "approved": False}],
            test_body="def test_x(): # AC-104\n    pass\n",
        )
        assert run(root) == 1, "onaysiz AC reddedilmeliydi"


def test_ac001_approved_without_approver_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(
            root,
            [{"ac_id": "AC-105", "approved": True, "approved_by": ""}],
            test_body="def test_x(): # AC-105\n    pass\n",
        )
        assert run(root) == 1, "approved_by bos ise reddedilmeliydi"


# ── AC-001 · Negatif: Gizli manifest test içeriği sızdıramaz ──────────────────
def test_ac001_hidden_manifest_rejects_non_ac_lines():
    """docs/02 §4.3 madde 2-3: manifest yalnız AC ID tutar, içerik sızdırmaz."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(
            root,
            [{"ac_id": "AC-106", "hidden": True}],
            test_body="# yok\n",
            hidden_manifest="AC-106\ndef test_secret_assertion(): assert x == 42\n",
        )
        assert run(root) == 1, "manifest'e test icerigi yazilmasi reddedilmeliydi"


# ── AC-001 · Negatif: Var olmayan AC'ye referans reddedilir ───────────────────
def test_ac001_orphan_test_reference_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(
            root,
            [{"ac_id": "AC-107"}],
            test_body="def a(): # AC-107\n    pass\ndef b(): # AC-999\n    pass\n",
        )
        assert run(root) == 1, "var olmayan AC'ye referans reddedilmeliydi"


# ── AC-001 · superseded AC hâlâ referans veriliyorsa uyarır (docs/06 §4) ──────
def test_ac001_superseded_ac_still_referenced_warns():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_repo(
            root,
            [{"ac_id": "AC-108", "status": "superseded"}],
            test_body="def test_x(): # AC-108\n    pass\n",
        )
        rep = cc.Report()
        cc.load_criteria(root / "specs/acceptance-criteria", rep)
        cc.scan_visible_tests(root, cc.DEFAULT_TEST_GLOBS, rep)
        cc.load_hidden_manifest(root / "tests/hidden/manifest.txt", rep)
        cc.evaluate(rep)
        assert any("superseded" in w for w in rep.warnings), "superseded uyarisi bekleniyordu"
        assert run(root) == 0, "superseded AC hata degil uyari olmaliydi"


# ── AC-001 · Ölçülebilir kısıt: bu repo üzerinde gerçekten yeşil ──────────────
def test_ac001_this_repo_passes_its_own_checker():
    repo = Path(__file__).resolve().parents[2]
    assert cc.main(["--root", str(repo), "--format", "text"]) == 0, (
        "repo kendi criteria coverage kuralini gecemedi"
    )


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  FAIL {name}: {exc}")
    print(f"\n{'BASARISIZ' if failures else 'GECTI'} — {failures} hata")
    sys.exit(1 if failures else 0)
