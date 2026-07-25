# AGENTS.md

> Bu dosya **bu repoda** çalışan ajan içindir.
>
> **Kendi projendeki/profilindeki ajanlara kural arıyorsan bu dosya değil:**
> - Proje kuralı (`AGENTS.md`) → [`harness/AGENTS.template.md`](harness/AGENTS.template.md)
> - Hermes profil kimliği (`SOUL.md`) → [`hermes/profiles/`](hermes/profiles/)

## Bu repo nedir

İki şablon barındırır, başka bir şey değil:

```
harness/AGENTS.template.md    proje kapsamlı kurallar (doldurulacak)
hermes/profiles/<rol>/SOUL.md ajan kapsamlı kimlik (hazır, 10 rol)
```

Kod yok, framework yok, kurulacak bir şey yok.

## Kurallar

**1. Kısa tut.** Bu repo bir kez fazla büyüdü ve kullanılamaz hale geldi.
Yeni dosya veya bölüm eklemek yerine mevcudu keskinleştir. Uzun kural dosyası
okunmaz — ajan 40 satırı uygular, 400 satırı görmezden gelir.

**2. Kapsam dışına çıkma.** Bu repo şablon barındırır. Doküman katmanı, araç,
CI, test, stack rehberi eklemek **kapsam dışıdır**. Gerekiyorsa önce sor.

**3. Somut ürün/proje adı yazma.** Şablonlar generic kalmalı. Örnek gerekiyorsa
davranış sınıfı yaz, proje adı değil.

**4. `SOUL.md` ile `AGENTS.md` sınırını koru.**

| `SOUL.md`'ye | `AGENTS.md`'ye |
|---|---|
| Ses, ton, doğrudanlık | Komut, path, port |
| Kararsızlık / itiraz davranışı | Dizin yasakları |
| Kanıt ve tamamlanma disiplini | Framework, iş akışı |
| Rolün sınırı — neye karışmadığı | Projeye özgü her şey |

Karar veremiyorsan sor: *"bu kural yarın başka bir projede de geçerli mi?"*
Evetse `SOUL.md`, hayırsa `AGENTS.md`.

**5. Araştırmadan yazma.** Bir iddia ekleyeceksen önce resmi/primary kaynağa bak,
sonra aynı konuyu Reddit'te ara. Kaynağı satırın yanına koy. Reddit anekdotunu
yaygınlık kanıtı sayma. Resmi doküman bir aracın nasıl davrandığını söyler;
senin ortamında kurulu olduğunu söylemez.

**6. Bu dosyayı ve `README.md`'nin giriş tablosunu değiştirme.** Giriş noktası,
sahibi insan.

## PR öncesi

```bash
# yerel markdown linkleri gerçekten var mı
python3 - <<'EOF'
import re, pathlib
fence, link = re.compile(r"^\s*```"), re.compile(r"\]\((?!https?:|#)([^)]+)\)")
for f in pathlib.Path(".").rglob("*.md"):
    if ".git" in f.parts: continue
    inside = False
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if fence.match(line): inside = not inside; continue
        if inside: continue
        for m in link.finditer(line):
            t = m.group(1).split("#")[0]
            if t and not (f.parent / t).exists():
                print(f"KIRIK {f}:{n} -> {m.group(1)}")
EOF

git diff --check
```

- [ ] Yeni dosya/dizin eklemedim (eklediysem sordum)
- [ ] Somut ürün/proje adı geçmiyor
- [ ] `SOUL.md`'ye proje kuralı sızmadı
- [ ] Kaynak linki desteklediği cümlenin yanında
