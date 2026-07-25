# Agentic Development

Bu depo, ajan tabanlı ve çok ajanlı geliştirme süreçleri için en iyi uygulamaları
belirlemeyi amaçlar.

Bir veya birden fazla ajanın; özellik geliştirme, hata giderme ve düzeltme gibi
görevleri otonom biçimde, talep edilen doğrultuda gerçekleştirmesini hedefler.
Ayrıca çok ajanlı sistemlerde ajanların birbiriyle çakışmasını veya birbirlerinin
değişikliklerini bozmasını önleyerek gereksinimlerin eksiksiz karşılanmasını
sağlamaya yönelik ilkeleri tanımlar.

---

## Ajan giriş noktası

**Bu dosyayı değiştirme.** Sahibi `agent:techlead` + insan (`docs/06-operations.md` §5.1).
Ajan kendi kısıtlarını yazamaz.

Kuralların tamamı: [`README.md`](README.md) → repo haritası. Üç eksen:
[sadakat](docs/02-spec-fidelity.md) · [çakışma](docs/03-concurrency.md) · [bütünlük](docs/04-codebase-integrity.md)

### Rolünü bul, kuralını oku

| Rolün | Zorunlu oku |
|---|---|
| **Engineer** (backend/frontend/mobile/unity/flutter) | `templates/TESTING.md` · `docs/03` §1–4 · `docs/04` §5, §7 · `docs/06` §6 |
| **QA** | `docs/02` §4 · `docs/05` §2, §4 · `docs/06` §3 |
| **Tech Lead** | `docs/02` tümü · `docs/03` tümü · `docs/04` tümü |
| **PM / Producer** | `templates/acceptance-criteria.md` · `docs/05` §2–3 · `docs/06` §4 |
| **Security** | `docs/02` §3.7 · `docs/06` §5 |
| **Designer** | `docs/05` §1 · ilgili `profiles/` |

Stack'in: [`profiles/backend.md`](profiles/backend.md) · [`profiles/flutter.md`](profiles/flutter.md) · [`profiles/unity.md`](profiles/unity.md)

---

## Her görevde, sırayla

```
1. CLAIM AÇ           görev + dokunacağın path'ler + TTL          → docs/03 §4
                      claim'siz PR reddedilir.
                      Path zaten claim'liyse BAŞLAMA — bekle veya böl.

2. GROUNDING          yazmadan önce ARA:                          → docs/04 §7
                      - search_graph(name_pattern=<niyet>)   aynı isimli var mı
                      - search_code(<davranış>)              aynı işi yapan var mı
                      - get_architecture()                   hangi katmana ait
                      Bulduysan KULLAN veya GENİŞLET, yeniden yazma.
                      Sonucu PR gövdesine yaz — yoksa PR reddedilir.

3. IMPACT ANALİZİ     dokunacağın sembollerden etkilenen testleri çıkar → docs/04 §5
                      Fast lane'de yalnız onları koş. PR'a yaz.
                      (Bu adım regresyonu %70 düşüren mekanizmadır.)

4. AC'yi OKU          approved: true mu? Değilse BAŞLAMA.         → docs/05 §3.2
                      Kapsam dışı bölümünü oku — kapsamı kendin genişletme.

5. YAZ                sahipliğin olan path'lerde, kendi worktree'nde → docs/03 §1–2
                      Değiştirdiğin davranışın eskisini SİL.        → docs/04 §6

6. FAST LANE          lokalde yeşil olmadan push etme (< 3 dk)     → docs/06 §1

7. PR AÇ              iki commit: test-only (A) + impl (B)         → docs/06 §2
                      CI kırmızı kanıtını KENDİSİ üretir; sen log üretmezsin.
```

---

## Pazarlıksız yasaklar

| ❌ | Referans |
|---|---|
| `tests/acceptance/**`, `tests/regression/**`, `tests/hidden/**`, `contracts/**` yazmak | `docs/02` §4.1–4.2 |
| Kilitli bir testi "düzeltmek" — 2. girişim spec gaming sinyalidir, durdurulur | `docs/05` §4 tahkim |
| Test değişikliğini üretim koduyla aynı PR'a koymak | `docs/02` §4.9 |
| `main`'e doğrudan push · force-push · history rewrite | `docs/06` §5.1 |
| Production erişimi · secret okuma/log'lama | `docs/06` §5.1 |
| `CODEOWNERS`, `ownership-map.yml`, `.github/workflows/**`, `AGENTS.md`, `.claude/**` değiştirmek | `docs/05` §5 |
| Lockfile · migration · generated kodu feature PR'ında commit etmek | `docs/03` §6 |
| Bağımlılık eklemek (`agent:deps` değilsen) | `docs/04` §4.1 |
| Sahipliğin olmayan path'e yazmak — istek aç | `docs/03` §1 |
| Aynı Unity sahnesinde başka açık PR varken çalışmak | `profiles/unity.md` §2 |
| Kapsamı kendi başına genişletmek veya küçültmek | `docs/06` §6.3 |

---

## Takıldığında — DUR ve escalate et

| Koşul | Eşik |
|---|---|
| Aynı fast lane hatası tekrar ediyor | 3 deneme |
| Toplam iterasyon | 10 |
| Süre / lease TTL | 4 saat |
| Aynı testi 2. kez düzeltmeye kalkışmak | 2 → spec gaming sinyali |
| Gizli set kırıldı | 1 → kendi başına düzeltmeyi DENEME, insana git |
| Claim çakışması | 1 |
| Kapsam dışına çıkma gereği | 1 |

Escalation formatı (`docs/06` §6.2) — **kısmi başarı beyan etme:**

```
- Hangi AC / görev
- NE BİTTİ      → CI çıktısına referansla, kendi beyanınla değil
- NE BİTMEDİ    → açıkça, telafi cümlesi olmadan
- Neden takıldın → son hata çıktısı
- Ne denedin
- Ne bıraktın   → branch, claim durumu, geri alınabilir mi
```

> **Temel kural:** Senin "bitti/geçti" demen ile CI'ın yeşil olması **iki farklı olaydır.**
> Yalnız ikincisi sayılır. Hiçbir gate senin beyanınla geçilmez — ajan raporu kanıt değildir
> (`docs/06` §5.3).
