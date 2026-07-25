# Profiller — stack ve proje spesifik eşlemeler

`docs/` altındaki kurallar **stack-agnostiktir.** Bu dizin onları somut araçlara eşler.

> **v1.0'da bu ayrım yoktu:** somut proje adları ve stack detayları ana dokümanın
> içine gömülüydü. Bu, dokümanı yeniden kullanılamaz kılıyordu — başka bir takım
> alıp uygulayamaz, kendi takımın da yeni bir proje eklediğinde ana dokümanı
> değiştirmek zorunda kalırdı. Profiller bu bağımlılığı kesiyor.

---

## Proje adı yasağı (ZORUNLU)

> **Bu repoda hiçbir yerde somut bir ürün/proje adı geçmez.** Ne `docs/`'ta, ne
> `templates/`'ta, ne profillerde, ne örneklerde, ne yorumlarda.

Profiller **teknoloji** ile adlandırılır (`flutter.md`, `unity.md`, `backend.md`),
ürün ile değil. Örnek gerekiyorsa **davranış sınıfı** yazılır, ürün değil:

| ❌ Yasak | ✅ Doğru |
|---|---|
| "\<ürün adı\> gibi tüketici uygulamasında" | "store dağıtımı yapılan uygulamalarda" |
| "\<oyun adı\> fizik testi" | "deterministik simülasyon / hesap zinciri" |
| "\<oyun adı\>'nda kural motoru" | "I/O'suz deterministik mantık" |
| "\<oyun adı\> vuruş hissi" | "kullanım hissi / etkileşim tepkisi" |

**Neden kural:** Proje adı içeren bir best-practice repo'su yeniden kullanılamaz —
ne başka bir takım alabilir, ne yeni bir proje eklendiğinde normatif doküman
değişmeden kalabilir. Kural setinin ömrü, adı geçen projelerin ömrüne bağlanmış olur.

Denetim (fast lane'e eklenebilir):

```bash
# proje adları için deny-list taraması — boş çıkmalı
grep -rniE '<yasakli-ad-1>|<yasakli-ad-2>' --include='*' . && exit 1 || true
```

## Mevcut profiller

| Profil | Kapsam |
|---|---|
| [`backend.md`](backend.md) | HTTP servisleri, contract testing, Testcontainers |
| [`flutter.md`](flutter.md) | Flutter/Dart, widget → golden → integration_test |
| [`unity.md`](unity.md) | Unity/C#, deterministik replay, **sahne/prefab çakışması** |

## Yeni profil yazma

Bir profil **yalnız eşleme yapar**, kural icat etmez. Kural `docs/`'ta yaşar.

Zorunlu bölümler:

1. **Test katmanı → araç eşlemesi** (`docs/02` §3'teki 17 türden hangileri geçerli)
2. **Architecture fitness function aracı** (`docs/04` §2)
3. **Impact analysis / etkilenen test seçimi aracı** (`docs/04` §5)
4. **Yüksek çekişmeli dosyalar** — bu stack'e özgü olanlar (`docs/03` §6)
5. **Fast lane komutu** ve süresi (`docs/06` §1)
6. **Bu stack'e özgü anti-pattern'ler**

Kural: profil `docs/`'taki bir kuralla çelişirse **`docs/` kazanır.** Profil
istisna talep ediyorsa ADR açılır (`templates/adr.md`).
