# TESTING.md — Test Taksonomisi (ajan skill dosyası)

> **Bu dosya ajanın context'ine girer.** Kopyala, projene göre doldur, `<...>` yerlerini değiştir.
>
> **Neden var:** Rehbersiz ajan repodaki baskın test desenini kopyalar. O desen kötüyse
> katlanarak kötüleşir — ajanlar 15 dakikalık integration test yığınları üretir
> (`docs/01-research.md` §1.1). Bu dosya o deseni sen seçersin diye var.
>
> **⚠ Eşik yazma kuralı:** Bu dosyaya mutation/coverage eşiği gibi **sayısal gate değerleri
> YAZMA** (`docs/07-metrics.md` §6). Ajan sayıyı görürse sayıyı optimize eder. Gate'i CI uygular.

---

## 1. Karar akışı — hangi testi yazacağım?

```
Yazdığım şey ne?
│
├─ Saf fonksiyon / karmaşık iş kuralı (I/O yok)
│    → UNIT.  Kural bir INVARIANT ise (para, skor, envanter, state machine)
│      → PROPERTY-BASED. Örnek değil kural test et.
│
├─ İki bileşen arasındaki dikiş (repo↔DB, servis↔queue, widget↔state)
│    → INTEGRATION / COMPONENT. Gerçek bağımlılık kullan (<Testcontainers/in-memory>).
│      Mock'la yalnız kontrol etmediğin dış sistemi (ödeme sağlayıcı, 3P API).
│
├─ Servis/istemci sınırı (HTTP, event, RPC)
│    → CONTRACT.  ⚠ Bunu SEN YAZMAZSIN — agent:techlead yazar. contracts/** kapalı.
│
├─ Bir AC-###'in kabul davranışı
│    → ACCEPTANCE.  ⚠ Bunu SEN YAZMAZSIN — agent:qa yazar. tests/acceptance/** kapalı.
│      (docs/02 §4.1: geçeceğin sınavı kendin yazmazsın)
│
├─ Uçtan uca kullanıcı yolculuğu
│    → E2E.  ⚠ agent:qa yazar. Toplam max <10> yolculuk. Kapsam aracı DEĞİL.
│
├─ Deterministik simülasyon / fizik / hesap zinciri
│    → REPLAY. Sabit seed + sabit timestep + kayıtlı input → final state hash.
│
└─ Görsel bileşen
     → önce DESIGN TOKEN DIFF, sonra (stabilse) GOLDEN. Ekran seviyesinde golden YAZMA.
```

## 2. Senin yazabildiklerin (Engineer ajanı)

| ✅ Yazabilirsin | ❌ Yazamazsın (write kapalı) |
|---|---|
| Unit | `tests/acceptance/**` |
| Integration / component | `tests/regression/**` |
| Property-based | `tests/hidden/**` |
| Replay | `contracts/**` |
| Kendi modülünün golden'ları | |

Kilitli bir testin yanlış olduğunu düşünüyorsan **düzeltmeye kalkışma** —
tahkim protokolünü izle (`docs/05-roles.md` §4). Kilitli teste 2. dokunma
girişimi spec gaming sinyali sayılır ve durdurulur (`docs/06` §6.1).

## 3. Zorunlu kurallar

1. **Her test bir `AC-###` etiketi taşır** (unit testler için kapsadığı AC).
   Etiket formatı: `<projedeki format, ör: test adında "[AC-042]">`
2. **Yeni test önce kırmızı olmalı.** CI bunu kendisi doğrular — sen log üretmezsin
   (`docs/06` §2). Yeni testin baştan yeşil çıkması PR'ı reddeder.
3. **Test değişikliği ile üretim kodu aynı PR'da olamaz** (`docs/02` §4.9).
4. **Değiştirdiğin davranışın eski implementasyonunu SİL.** "İhtiyaten bıraktım" yasak
   (`docs/04` §6).
5. **Yazmadan önce ara** — grounding sorgusu zorunlu (`docs/04` §7). Sonucunu PR'a yaz.
6. **Etkilenen testleri çıkar** — impact analizi zorunlu (`docs/04` §5). PR'a yaz.

## 4. Anti-pattern'ler — YASAK

| ❌ | Neden |
|---|---|
| Framework internals'ı test etmek | Framework'ün işi, senin değil |
| Config değeri test etmek (`assert TIMEOUT == 30`) | Tautoloji, sıfır bilgi |
| Exact HTML/string assert etmek | Kırılgan, davranış değil biçim test eder |
| Mock'un çağrıldığını assert etmek (davranış yerine) | Implementasyonu dondurur, refactor'u öldürür |
| Her şeyi mock'lamak | Dikişleri test edilmemiş bırakır — gerçek hatalar orada |
| `assert True` / assert'siz test | Coverage'ı şişirir, hiçbir şey doğrulamaz. Mutation gate yakalar. |
| Aynı davranış için 5 unit test varyantı | Ajanın "coşkulu test yazarı" modu. Kural test edeceksen property-based yaz. |
| Test içinde `sleep` | Flake üretir → ajana test zayıflatmayı öğretir (`docs/06` §3) |
| Testler arası paylaşılan mutable state | Sıra bağımlılığı = flake |
| Retry ile kırmızıyı gizlemek | Flake'i maskeler, sinyali bozar |
| Ekran seviyesinde screenshot golden | Pixel diff cehennemi |
| E2E'yi kapsam aracı olarak kullanmak | Pahalı + kırılgan; max <10> yolculuk |
| Yeni test dizini/altyapısı icat etmek | Mevcut taksonomiyi kullan; değişiklik gerekiyorsa Tech Lead'e sor |

## 5. Proje spesifik

| | |
|---|---|
| Test komutu (hepsi) | `<...>` |
| Test komutu (impact-seçilmiş) | `<ör: jest --findRelatedTests, pytest-testmon>` |
| Fast lane lokal komutu | `<...>` — push etmeden önce yeşil olmalı |
| Unit dizini | `<...>` |
| Integration dizini | `<...>` |
| Fixture/factory konumu | `<...>` |
| Gerçek bağımlılık altyapısı | `<Testcontainers / in-memory / emulator>` |
| Property-based kütüphanesi | `<Hypothesis / fast-check / glados>` |
| Mock'lanması ONAYLI dış sistemler | `<liste>` |
| Bilinen flaky testler (karantina) | `<liste + TTL>` |
