# Hedef repo için `AGENTS.md` — kopyala, doldur, bitti

Aşağıdaki bloğu **kendi projenin köküne `AGENTS.md` olarak kopyala**, `<...>` yerlerini doldur.
Başka hiçbir dosyayı okumana gerek yok. Bu blok tek başına çalışır.

> Neden kısa: uzun kural dosyası okunmaz. Ajan 40 satırı uygular, 400 satırı görmezden gelir.
> Önce Seviye 1'i koy, çalıştığını gör, sonra gerekiyorsa Seviye 2'yi ekle.

---

## Seviye 1 — Tek ajanla çalışıyorsan (bununla başla)

````markdown
# AGENTS.md

Proje: <bir cümle: ne yapan uygulama>
Stack: <dil/framework>

## 1. Yazmadan önce ara

Yeni fonksiyon, servis veya yardımcı yazmadan önce **mevcut kodda ara**.
Varsa kullan veya genişlet — yeniden yazma.
PR açıklamasına ne aradığını ve ne bulduğunu yaz.

## 2. Kapsamı aşma

Sadece görevin gerektirdiği dosyalara dokun.
İstenmeyen refactor, "bu arada şunu da düzelttim", stil değişikliği yapma.
Kapsamı genişletmek gerekiyorsa **dur ve sor**.

## 3. Testler

- Yazabilirsin: `<unit/integration test dizini, ör: tests/unit/>`
- **Yazamazsın / değiştiremezsin:** `<kabul testi dizini, ör: tests/acceptance/>`
  Bunlar senin geçmen gereken sınav. Kendi sınavını yazamazsın.
- Var olan bir testi zayıflatarak/silerek yeşile getirme.
  Test gerçekten yanlışsa **DUR ve söyle** — kendin düzeltme.
- Yeni davranış yazdıysan testi de yaz.

## 4. Push etmeden önce

```bash
<komut>   # lint + tip kontrolü + build
<komut>   # testler
```

Bu ikisi yeşil değilse push etme. CI'ı deneme-yanılma aracı olarak kullanma.

## 5. Asla

- `main`'e doğrudan push · `--force` push · history rewrite
- Production erişimi · secret okuma, yazma veya log'lama
- `<lockfile, ör: package-lock.json>` veya `<migration dizini>` değişikliğini
  feature PR'ına koymak — bunlar **ayrı PR**
- Yeni bağımlılık eklemek (önce sor)
- Bu dosyayı (`AGENTS.md`) veya CI ayarlarını değiştirmek

## 6. Takılırsan

Aynı hata 3 kez tekrarlandıysa **DUR**. Şunu raporla:

- Ne bitti — test/komut çıktısıyla, "bitti" demenle değil
- Ne bitmedi — açıkça, telafi cümlesi olmadan
- Son hata çıktısı
- Ne denedin

Bitmediyse "tamamlandı" yazma. Yarım işi tam göstermek en pahalı hata.

## 7. PR açıklamasında olacaklar

- Ne aradın, ne buldun (madde 1)
- Hangi mevcut testler bu değişiklikten etkilenir
- **Neyi yapmadın** ve neden
````

---

## Seviye 2 — Birden fazla ajan aynı repoda çalışıyorsa

Seviye 1'in sonuna **ek olarak** şunu koy:

````markdown
## 8. Paralel çalışma

### Kendi çalışma alanında çalış
```bash
git worktree add ../wt-<gorev> -b agent/<gorev>
```
Ortak dizinde çalışmayın — birbirinizin yarım işini görür ve üstüne yazarsınız.
Not: worktree **dosyaları** ayırır; port, veritabanı, `.env` ve cache hâlâ ortak.
Bunları da ayır: `<nasıl, ör: her worktree için farklı port/DB adı>`

### Başlamadan önce yerini bildir
Dokunacağın dosyaları `<yer, ör: GitHub issue / tasks/active/ dizini>` içine yaz.
Aynı dosyayı başkası almışsa **BAŞLAMA** — bekle veya görevi böl.

### Sahiplik
| Dizin/dosya | Sahibi |
|---|---|
| `<src/api/>` | `<ajan/kişi>` |
| `<src/ui/>` | `<ajan/kişi>` |
| `<migration dizini>` | `<tek sahip>` |
| `<lockfile>` | `<tek sahip>` |

Sahibi olmadığın yere yazma — istek aç.

### Şu dosyalara aynı anda iki kişi dokunamaz
`<lockfile>` · `<migration>` · `<üretilen kod: *.g.dart, protobuf vb.>` ·
`<merkezi route/DI/registry dosyası>` · `<Unity sahne/prefab varsa>`

Bunlar merge edilemez veya sessizce bozulur. Sıra ile, ayrı PR'larda.

### Şema/arayüz önce dondurulur
Ortak bir API/şema değişiyorsa: önce şema tek başına merge edilir,
**sonra** ona bağlı işler paralel başlar. İki kişi aynı şemayı tasarlamaz.

### Merge
`main`'e merge queue / rebase ile. "Bende yeşildi" yeterli değil —
iki değişiklik ayrı ayrı yeşil olup birleşince kırılabilir.
````

---

## Doldurma kılavuzu

| Yer | Ne yazacaksın | Bilmiyorsan |
|---|---|---|
| Proje / Stack | Bir cümle + dil/framework | — |
| Test dizinleri | Hangisi ajana açık, hangisi kapalı | Kapalı diye bir şey yoksa madde 3'ün 1–2. satırını sil, gerisini bırak |
| Push öncesi komutlar | Projenin gerçek lint + test komutları | `package.json` / `Makefile` içine bak |
| Lockfile | `package-lock.json` · `pubspec.lock` · `Podfile.lock` · `Cargo.lock` | Repo kökünde `*.lock` ara |
| Migration dizini | DB migration'larının yeri | Yoksa maddeden çıkar |
| Sahiplik tablosu | Tek ajan varsa Seviye 2'yi hiç ekleme | — |

**Kural:** Doldurmadığın satırı **sil**. `<...>` bırakılmış bir kural, kural değildir — ajan onu atlar.

---

## Nasıl bilirsin işe yaradığını

İlk hafta şu üçünü say:

1. Ajan kapalı test dizinine kaç kez dokunmaya çalıştı → 0 olmalı
2. Kaç PR "bitti" dedi ama aslında bitmemişti → düşmeli
3. İki ajan kaç kez aynı dosyada çakıştı → sahiplik tablosu çalışıyor mu

Bu üçü iyiyse dosya işini yapıyor. Değilse **eksik olan maddeyi** ekle — dosyayı büyütmek değil, doğru maddeyi bulmak önemli.

---

Hermes profil kimliği (`SOUL.md`) tarafı için: [`../hermes/profiles/`](../hermes/profiles/)
