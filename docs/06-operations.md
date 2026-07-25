# 06 — Operasyon: CI, Döngü Süresi, Spec Değişimi, Güvenlik Sınırları, Escalation

> **Normatif rehber önerisi.** Bu bölüm hedef repo operasyonunu anlatır; bu
> Markdown rehberinin kendi CI/TDD mimarisi değildir.

---

## 1. CI mimarisi — döngü süresi birinci sınıf kısıttır

### 1.1 Problem

v1.0'ın CI sırası merge gate'ine kadar **~26 dakika**, E2E dahil ~36 dakika sürüyordu. İnsan takımı için kabul edilebilir; **otonom ajan döngüsü için felaket.** Ajan hata → düzelt → tekrar döngüsünde her iterasyon 26 dakika sürerse ajanın hız avantajı tamamen yok olur. Otonom sistemde **cycle time birincil kısıttır**, gate sayısı değil.

### 1.2 Üç şeritli model

```
┌─ FAST LANE ───────────────────────────── repo p95 SLO ─┐
│ ajan her push'ta koşar, ajan çıktısını GÖRÜR          │
│                                                        │
│ 1. Statik kapılar (tip + lint + derleme)      ~30 sn  │
│ 2. Architecture fitness functions            ~10 sn  │
│ 3. Secret scan (diff)                        ~10 sn  │
│ 4. IMPACT-SEÇİLMİŞ testler (tam suite DEĞİL) ~60 sn  │  ← 04 §5
│ 5. Contract şema doğrulama (diff)            ~20 sn  │
│ 6. Criteria coverage checker                  ~5 sn  │  ← tools/
└────────────────────────────────────────────────────────┘
                          ▼  yeşilse PR açılabilir
┌─ MERGE LANE ──────────────────────────── repo p95 SLO ┐
│ PR review-ready olduğunda                             │
│                                                        │
│  7. Tam unit + property suite                 ~2 dk   │
│  8. Integration (Testcontainers)              ~5 dk   │
│  9. Acceptance / BDD (görünür set)            ~4 dk   │
│ 10. Contract diff / oasdiff (breaking → G3)   ~1 dk   │
│ 11. SAST (değişen dosyalar)                   ~2 dk   │
│ 12. Incremental mutation (diff)               ~3 dk   │  ← 02 §4.4
│ 13. Repo-kalibreli diff coverage              ~1 dk   │
│ 14. Duplikasyon + API surface diff            ~1 dk   │  ← 04 §3-4
│ 15. Kırmızı kanıtı (CI üretir)                ~1 dk   │  ← §2
│ 16. Risk sınıflandırma → G2 gerekiyor mu      ~5 sn   │  ← 05 §3.3
└────────────────────────────────────────────────────────┘
                          ▼
┌─ MERGE QUEUE / merge_group ────────────────────────────┐  ← 03 §5
│ sentetik birleşik SHA üzerinde 7–16 DAHİL tüm required │
│ check'ler tekrar koşar                                  │
│ 17. DIŞ/İZOLE hidden evaluator required check          │  ← 02 §4.3
│ 18. E2E kritik yolculuklar                              │
└────────────────────────────────────────────────────────┘
                          ▼  main
┌─ NIGHTLY / WEEKLY (gate değil, trend) ─────────────────┐
│ Tam mutation suite · DAST · perf bütçesi · full E2E    │
│ Ölü kod trendi · bağımlılık CVE taraması               │
└────────────────────────────────────────────────────────┘
```

Şemadaki süreler örnek bütçedir, taşınabilir eşik değildir. İlk pilotta her
adımın p50/p95 süresi ölçülür; stack'e özgü SLO ve shard/cache kararı bu
baseline'dan çıkar.

### 1.3 Hız kuralları

| Kural | Gerekçe |
|---|---|
| **Fast lane yeşil olmadan push/PR yok** — lokalde de koşabilir olmalı | Ajanın CI'ı deneme-yanılma aracı olarak kullanmasını engeller |
| **Fast lane tam suite koşmaz**, impact-seçilmiş alt küme koşar | Hem hız hem doğruluk → [`04` §5](04-codebase-integrity.md) |
| **Fast lane repo p95 SLO'sunu aşarsa optimizasyon işi açılır** | Cycle time gate'lerden önce gelir; SLO baseline sonrası sürümlenir |
| **Paralel shard** | Suite büyüdükçe süre sabit kalmalı |
| **Normal merge_group log'u görünür, hidden evaluator ham log'u kapalıdır** | Debug edilebilirlik korunur; yalnız hidden oracle sızmaz |

---

## 2. Kırmızı kanıtı — CI üretir (implementasyon)

Neden ajanın ürettiği log kanıt değil: [`02` §4.5](02-spec-fidelity.md). Mekanizma:

```
Yeni kilitli oracle içeren integration PR:
  commit A : QA-imzalı, yalnız izinli oracle path'leri
  commit B : Engineer implementasyonu

Adapter CI:
  1. commit sırasını, yazar rolünü ve path saflığını doğrular
  2. base + commit A state'inde yalnız yeni test kimliğini çalıştırır
  3. beklenen ASSERTION FAILURE sınıfını doğrular
     syntax/import/setup/timeout/altyapı hatası → GEÇERSİZ KANIT
  4. HEAD state'inde aynı test kimliği yeşil olmalıdır
  5. sonucu CI attestation'ına yazar
```

Generic “komut non-zero döndü” mekanizması güvenli değildir. Test kimliği ve failure
Sınıf framework adapter'ıyla doğrulanmadıkça kırmızı kanıt mekanizması yalnız
pilot önerisidir.
Mevcut kilitli oracle değişikliği ayrı PR'dır; Engineer unit/integration testleri
ise üretim koduyla aynı PR'da olabilir.

Kapsam: acceptance + regresyon + bug-fix PR'ları. Saf refactor PR'ları muaf (davranış değişmiyor → yeni test yok).

---

## 3. Flaky test politikası (ZORUNLU)

**Otonom sistemde flake normal bir sıkıntı değil, güvenlik açığıdır:** ajan, kırmızıyı "düzeltmek" için testi zayıflatır. Flaky bir test, ajana test zayıflatmayı öğretir.

| Kural | Detay |
|---|---|
| **Tespit** | Aynı commit'te 2 koşumdan farklı sonuç, veya son 20 koşumda ≥2 tutarsızlık |
| **Kontrollü karantina** | Tespit edilen test ayrı quarantine lane'e alınır. Kritik AC'nin tek oracle'sıysa replacement olmadan required gate'ten çıkarılamaz. |
| **Sahip ataması zorunlu** | Karantina anında test sahibine (QA veya Engineer) görev açılır |
| **Karantina TTL** | Repo policy'sinde kalibre edilir. Süre dolunca release/merge gate'i bloke edilir ve insana escalate edilir; test otomatik silinmez. |
| **Ajan flaky testi değiştiremez** | Karantinadaki test test sahibinin sorumluluğunda |
| **Metrik** | Flake oranı baseline'a göre yükseliyorsa CI güvenilirliği işi açılır |

**Anti-pattern:** Retry ile flake gizlemek. Retry, flake'i *maskeler* ve ajanın gördüğü sinyali bozar. Retry yalnız bilinen dış bağımlılık (network) için, açık gerekçeyle.

---

## 4. Spec değişim protokolü (ZORUNLU)

v1.0'da yalnız "spec-change PR açar" diye geçiyordu; protokol yoktu. Multi-agent'ta bu bir **yarış durumudur**: Ajan A, AC-042 v1'e göre kod yazarken PM AC-042'yi v2'ye taşırsa, A'nın işi sessizce geçersizleşir.

### 4.1 AC versiyonlama

Her AC'de `version` ve `supersedes` alanı bulunur. AC dosyası **hiç silinmez**, `status: superseded` olur — testler ID referansı taşıdığı için silinen AC öksüz test üretir.

### 4.2 Değişim akışı

```
1. Değişiklik talebi (PM ajanı veya Engineer'ın "spec eksik" bulgusu)
2. PM ajanı AC-###'i v(n+1) olarak yazar, delta'yı açıkça listeler
3. ╔ İNSAN ONAYI (G4) ╗                                    ← 05 §3.2
4. Etki analizi — ZORUNLU:
     a) Bu AC'yi hangi testler referans veriyor
     b) O testler hangi kodu kapsıyor
     c) O path'lerde AÇIK CLAIM var mı                     ← 03 §4
5. Açık claim varsa → INVALIDATION BİLDİRİMİ gönderilir     ← 03 §4.3
     Ajan durur, yeni AC'yi okur, işini yeniden değerlendirir.
     "Devam edip sonra uydururuz" YASAK.
6. QA ajanı acceptance testini v(n+1)'e günceller (ayrı PR)  ← 02 §4.9
7. Engineer implement eder
8. Eski v(n) testi silinir; criteria coverage v(n+1)'i talep eder
```

### 4.3 Kural

> **Bir AC, ona bağlı açık claim varken sessizce değiştirilemez.** Değişim ya bildirimle olur ya da claim kapanana kadar bekler.

Şablon: [`templates/spec-change.md`](../templates/spec-change.md)

---

## 5. Ajan yetki sınırları / blast radius (ZORUNLU)

v1.0 güvenliği yalnız *ürettiği kodun* güvenliği olarak ele alıyordu (SAST/SCA/authz). Ama atıf yaptığı arXiv 2605.30777'nin baskın risk kategorileri: constraint violation, **destructive operations**, authorization bypass, **deception**. Yani ajanın *kendi eylemleri* de risk yüzeyi — ve *otonom* bir sistem için bu bölüm olmadan olmaz.

### 5.1 Pazarlıksız yasaklar

| ❌ YASAK | Sebep |
|---|---|
| Production ortamına herhangi bir erişim | Geri dönüşü yok |
| Production veritabanına yazma (okuma da varsayılan kapalı) | PII + geri dönüşsüzlük |
| `git push --force` (paylaşılan branch) | History kaybı |
| History rewrite (`filter-branch`, `reset --hard` uzakta) | Aynı |
| Branch/tag silme (uzakta) | Aynı |
| `main`'e doğrudan push | → [`03` §5](03-concurrency.md) |
| Secret okuma / yazma / log'lama | Sızıntı |
| CI/CD konfigürasyonunu kendi PR'ında değiştirmek | Gate'i kendi lehine değiştirme |
| `CODEOWNERS`, `ownership-map.yml`, `.claude/**`, `AGENTS.md` değiştirmek | Kural sahibi kendisi olamaz → [`05` §5](05-roles.md) |
| Çalışma dizini dışına yazma | Ortam hasarı |
| Kayıtlı olmayan dış servise veri gönderme | Sızıntı |
| Bağımlılık ekleme (`agent:deps` dışında) | → [`04` §4.1](04-codebase-integrity.md) |

### 5.2 Onay gerektirenler

Ajan yapabilir ama **insan onayı** ister: migration çalıştırma (staging bile), toplu dosya silme (> 10 dosya), dizin taşıma/rename, yeni dış servis entegrasyonu, ödeme/faturalama koduna dokunma, yeni top-level dizin.

### 5.3 Yapısal önlemler

| Önlem | Detay |
|---|---|
| **Sandbox** | Ajan konteyner/VM içinde. Yasakları temenniye bırakma, **çalıştıramaz** hale getir. |
| **En az yetki token'ı** | Feature ajanının token'ı yalnız kendi branch'ine push edebilir |
| **Ayrı ortam** | Staging bile ajana ayrı. Ortak staging'i bozan ajan tüm takımı durdurur. |
| **Denetim log'u** | Ajanın çalıştırdığı her komut kaydedilir. "Fabricated success report" ancak bağımsız log'la yakalanır. |
| **Ajan raporu ≠ kanıt** | Genel kural: ajanın "yaptım/geçti" beyanı hiçbir gate'i geçirmez. Gate'i CI'ın kendi ölçümü geçirir. |

---

## 6. Escalation ve durma koşulları (ZORUNLU)

"Otonom" iddiası, ajanın **takıldığında ne yaptığı** tanımlanmadan geçerli olamaz. v1.0'da yoktu.

### 6.1 Durma koşulları

| Koşul | Eşik | Aksiyon |
|---|---|---|
| Aynı fast lane hatası tekrar ediyor | 3 deneme | DUR, insana escalate |
| Toplam iterasyon | 10 | DUR, kısmi işi rapor et |
| Süre | Aktif lease'in `lease_expires` değeri | DUR; fencing varsa yeni token ile release, yoksa insan tahkimi |
| Aynı testi 2. kez "düzeltmeye" kalkışıyor | 2 | DUR — spec gaming sinyali, insana escalate |
| Gizli set kırıldı | 1 | DUR — ajan kendi başına düzeltmeyi denemez, insana gider ([`05` §4](05-roles.md)) |
| Claim çakışması | 1 | DUR, bekle veya böl ([`03` §4.2](03-concurrency.md)) |
| Token/maliyet bütçesi | §7 | DUR |
| Kapsam dışına çıkma gereği belirdi | 1 | DUR — kapsamı kendi genişletmez |

### 6.2 Escalation formatı (ZORUNLU)

Ajan durduğunda **kısmi başarı beyan etmez.** Şunları rapor eder:

```
- Hangi AC / görev
- NE BİTTİ (test kanıtıyla — CI çıktısına referans, kendi beyanı değil)
- NE BİTMEDİ (açıkça, telafi cümlesi olmadan)
- Neden takıldı — son hata çıktısı
- Ne denendi (deneme listesi)
- Ne bırakıldı: branch, claim durumu, geri alınabilir mi
```

**Kural:** Yarım işi "tamamlandı" olarak raporlamak, ölçülmüş bir ajan hata modudur (*fabricated success reports*, arXiv 2605.30777). Escalation formatı bunu yapısal olarak zorlaştırır. Bir ajanın "bitti" demesi ile CI'ın yeşil olması **iki farklı olaydır**; yalnız ikincisi sayılır.

### 6.3 Kısmi iş politikası

Kapsamın bir kısmı bloke olduysa: **geri kalanı tamamla**, bloke olanı açıkça belirt. Kapsamı kendi başına küçültmek yasaktır — küçültme kararı insanın.

---

## 7. Maliyet bütçesi

v1.0'da hiç yoktu. Otonom sistemde maliyet sessizce büyür.

| Bütçe | Ne | Aksiyon |
|---|---|---|
| Token / görev | Rol başına tavan | Aşımda escalate (§6.1) |
| CI dakikası / PR | Fast lane + merge lane tavanı | Aşımda suite optimizasyonu işi |
| İterasyon / görev | 10 | §6.1 |
| Paralel ajan sayısı | Çekişmeye göre — [`03` §8](03-concurrency.md) | Fazla paralellik *yavaşlatır* |

**Ölçülecek:** merge edilmiş AC başına maliyet. Reddedilen/çöpe giden iş de maliyettir; asıl optimize edilecek sayı budur.
