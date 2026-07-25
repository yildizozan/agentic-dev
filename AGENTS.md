# AGENTS.md

> ⚠ **Bu dosya bu rehber repo'sunda çalışan ajan içindir** — yani rehber
> içeriğini düzenleyen ajan.
>
> **Kendi projendeki ajanlara kural arıyorsan bu dosya değil:**
> → **[`templates/AGENTS.md`](templates/AGENTS.md)** (kopyala-yapıştır, tek dosya)

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

Kod testi veya TDD gerekmez. PR öncesi:

```bash
# yerel linkler sağlam mı
grep -roE '\]\([^)h][^)]*\)' --include='*.md' . | head -50   # gözle kontrol
python3 tools/criteria_coverage.py                            # varsa yeşil kalsın
git diff --check                                              # whitespace
```

Kontrol listesi:

- [ ] Kaynak linki, desteklediği cümlenin yanında mı?
- [ ] Reddit bulgusu "anekdot/saha sinyali" diye etiketli mi?
- [ ] Paper sonucu model + örneklem + tarih bağlamıyla mı yazılı?
- [ ] Somut proje/ürün adı geçmiyor mu?
- [ ] Yeni bir kural eklediysen, gerekçesi ve sınırı yazılı mı?
