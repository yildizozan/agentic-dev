# AGENTS.md

> ⚠ **Bu dosya bu rehber repo'sunda çalışan ajan içindir** — yani rehber
> içeriğini düzenleyen ajan.
>
> **Kendi projendeki/profilindeki ajanlara kural arıyorsan bu dosya değil:**
> - Proje kuralı (`AGENTS.md`) → **[`harness/AGENTS.template.md`](harness/AGENTS.template.md)**
> - Hermes profil kimliği (`SOUL.md`) → **[`hermes/SOUL.template.md`](hermes/SOUL.template.md)**

---

## Bu repo nedir

Ajanlarla yazılım geliştirme için bir **Markdown rehberi**. Kod ürünü yok,
kurulacak bir şey yok. Ürün: kaynakları izlenebilir, sınırlılıkları dürüst içerik.

## Rehbere katkı yaparken

### 1. Araştırmadan yazma

Herhangi bir anlamlı içerik değişikliğinden önce:

1. **Resmi/primary kaynak** ara (vendor dokümanı, paper, araç dokümanı).
2. **Aynı konuyu Reddit'te** ara — çözüm kopyalamak için değil, gerçek failure
   mode ve ergonomi riskini görmek için.
3. Sorguyu, tarihi ve bulguyu `docs/09-web-reddit-field-guide.md` §6'ya kaydet.

Kanıt hiyerarşisi: **resmi kaynak > ampirik araştırma > Reddit anekdotu > sentez.**
Reddit gönderisi prevalans veya nedensellik kanıtı değildir; hipotez üretir.
Doğrulanamayan bir kaynağı yeni bir kuralın **tek** gerekçesi yapma.

### 2. Somut proje/ürün adı yazma

Rehber generic kalmalı. Profiller **teknoloji** adıyla anılır (`flutter.md`,
`unity.md`, `backend.md`), ürün adıyla değil. Örnek gerekiyorsa davranış sınıfı
yaz ("deterministik simülasyon", "store dağıtımı yapılan uygulamalar").

### 3. Dili dürüst tut

- Ölçülmemiş bir şeyi ölçülmüş gibi yazma. Benchmark yüzdesini eşik yapma.
- Bir öneri hedef repoda pilot gerektiriyorsa "pilot önerisi" de, "kural" deme.
- Bir mekanizmanın sınırını sakla­ma (ölçüldüğü model, örneklem, tarih).

### 4. Kısa tut

Bu repo bir kez fazla büyüdü ve kullanılamaz hale geldi. Yeni bölüm eklemek
yerine mevcut bölümü keskinleştir. Uzun kural dosyası okunmaz.

### 5. Değiştirme

- Bu dosya (`AGENTS.md`) ve `README.md`'nin "Buradan başla" bölümü — giriş
  noktası, sahibi insan.
- Geçmişteki kaynak kayıtlarını silme; yanlışsa düzeltme notu ekle.

## Doğrulama

Bu repo Markdown üretir; kod testi veya TDD gerekmez. PR öncesi:

```bash
# 1. yerel markdown linkleri gerçekten var mı  (kod bloklarını atlar)
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

# 2. whitespace
git diff --check

# 3. proje adı yasağı (madde 2) — deny-list'i kendin doldur, repoya yazma
grep -rniE 'yasakli-ad-1|yasakli-ad-2' --include='*.md' . && echo IHLAL
```

Kontrol listesi:

- [ ] Kaynak linki, desteklediği cümlenin yanında mı?
- [ ] Reddit bulgusu "anekdot/saha sinyali" diye etiketli mi?
- [ ] Paper sonucu model + örneklem + tarih bağlamıyla mı yazılı?
- [ ] Somut proje/ürün adı geçmiyor mu?
- [ ] Yeni bir kural eklediysen, gerekçesi ve sınırı yazılı mı?
