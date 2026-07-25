# Profiller — stack ve proje spesifik eşlemeler

`docs/` altındaki kurallar **stack-agnostiktir.** Bu dizin onları somut araçlara eşler.

> **v1.0'da bu ayrım yoktu:** somut proje adları ve stack detayları ana dokümanın
> içine gömülüydü. Bu, dokümanı yeniden kullanılamaz kılıyordu — başka bir takım
> alıp uygulayamaz, kendi takımın da yeni bir proje eklediğinde ana dokümanı
> değiştirmek zorunda kalırdı. Profiller bu bağımlılığı kesiyor.

---

## Ürün bağlamı ve yeniden kullanılabilirlik

Çekirdek `docs/` ve `templates/` üründen bağımsız kalır. Profiller
teknoloji ile adlandırılır (`flutter.md`, `unity.md`, `backend.md`), ürün ile
değil.

Vaka çalışmaları ve ölçüm raporları ise kanıtın bağlamını kaybetmemelidir.
Paylaşım izni varsa ürün/proje adı veya anonim bir vaka kimliği kullanılabilir;
model, stack, dönem ve görev dağılımı mutlaka kaydedilir. Örnek genellenebilir
bir kuralı açıklıyorsa davranış sınıfı tercih edilir:

| ❌ Yasak | ✅ Doğru |
|---|---|
| "\<ürün adı\> gibi tüketici uygulamasında" | "store dağıtımı yapılan uygulamalarda" |
| "\<oyun adı\> fizik testi" | "deterministik simülasyon / hesap zinciri" |
| "\<oyun adı\>'nda kural motoru" | "I/O'suz deterministik mantık" |
| "\<oyun adı\> vuruş hissi" | "kullanım hissi / etkileşim tepkisi" |

Ürün adını otomatik deny-list ile yasaklamak yerine gizlilik ve lisans kuralları
uygulanır. Aksi halde gerçek pilot kanıtı bağlamından kopar ve denetlenemez hale
gelir.

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
