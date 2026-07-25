# 02 — Spec Sadakati: Spec → Test Zinciri

> **Normatif.** Bu dosyadaki `ZORUNLU` / `YASAK` ifadeleri CI tarafından uygulanır.
> Kapsam: ajanın *istenen davranışı* ürettiğinin garantisi.
> Kapsam **dışı**: ajanların birbirini bozması → [`03`](03-concurrency.md) · codebase çürümesi → [`04`](04-codebase-integrity.md)

---

## 1. Temel tez

**Spec tek başına yetmez.** Prose spec ajanın *niyetini* hizalar; sadakati sadece **çalıştırılabilir oracle** garanti eder. Spec'in doğrulanmadığı her satır drift eder.

**En yüksek kaldıraç:** kabul kriteri ↔ test 1:1 eşlemesi ve contract testleri — çünkü bunlar spec'in *kendisi* olur, spec *hakkında* yazılmış bir belge olmaz.

**Asıl risk test eksikliği değil, test oyunlaştırmasıdır.** Ajan testi geçmek yerine testi değiştirmeyi öğrenir. Bunu ancak §4'teki kontroller durdurur.

---

## 2. Sadakat zinciri

```
Vizyon / Constitution
        │
        ▼
   PRD / Feature Spec                          (PM ajanı yazar)
        │
        ▼
   Kabul Kriteri  AC-###                       (PM ajanı yazar)
        │
        ▼
   ╔═══════════════════════════╗
   ║  İNSAN ONAY GATE'İ  (G1)  ║               ← zincirdeki tek ground truth
   ╚═══════════════════════════╝                 bkz. 05 §3
        │
        ▼
   Gherkin senaryo → çalıştırılabilir acceptance test   (QA ajanı otomatize eder)
        │
        ├──────────────┬───────────────┬──────────────┐
        ▼              ▼               ▼              ▼
  Contract/Şema   Integration       Unit      Architecture fitness
  (Tech Lead)      (Engineer)    (Engineer)      (Tech Lead)
        │              │               │              │
        └──────────────┴───────┬───────┴──────────────┘
                               ▼
                    CI Fast Lane  (< 3 dk)                bkz. 06 §1
                               ▼
                    CI Merge Lane
                               ▼
                    ╔═══════════════════╗
                    ║   MERGE QUEUE     ║               bkz. 03 §5
                    ╚═══════════════════╝
                               ▼
                 Gizli test seti + incremental mutation
                        (QA)              (Tech Lead)
                               ▼
                          main
```

### 2.1 Altın kural (ZORUNLU)

> Her `AC-###` için, **görünür test suite'inde veya gizli set manifest'inde** o ID'yi referans veren en az bir test bulunmak ZORUNLUDUR. Bulunmuyorsa build kırmızıdır.

Bu, "coverage" değil **kriter kapsaması (criteria coverage)** ölçer. Uygulayan: [`tools/criteria_coverage.py`](../tools/criteria_coverage.py).

> **Not — v1.0'daki çelişki düzeltilmiştir.** Önceki sürüm "her AC'nin CI'da testi olmalı" derken aynı zamanda AC'lerin %20–30'unun testini ajanın göremeyeceği yerde tutuyordu; checker bunları kaçınılmaz olarak "0 test" diye raporlardı. Çözüm: gizli set, **içerik sızdırmadan yalnız AC ID listesi** yayınlar (`tests/hidden/manifest.txt`). Checker onu da okur. Böylece kapsama ölçülebilir, test içeriği gizli kalır.

### 2.2 AC formatı

Şablon: [`templates/acceptance-criteria.md`](../templates/acceptance-criteria.md). Zorunlu alanlar: ID, başlık, Gherkin senaryo(lar)ı, negatif senaryolar, kapsam dışı, `hidden: true|false`, onaylayan insan, spec versiyonu.

---

## 3. Test türleri — önem sıralaması

**Skala okuma notu:** Etki/Kurulum/Bakım sayıları **kalibre edilmiş yargıdır, ölçüm değildir.** Tartışmayı yapılandırmak için var; kanıt olarak sunulmamalı. Pilot sonrası kendi verinle güncelle.

Etki = spec sadakatine katkı (1–5) · Kurulum = ilk kurulum eforu (1=çok az) · Bakım = süregelen kırılganlık maliyeti.

| # | Test türü | Etki | Kur. | Bakım | Sahip | Neden bu sırada |
|---|---|:--:|:--:|:--:|---|---|
| 1 | **Acceptance / BDD senaryo** (Gherkin, AC başına ≥1) | 5 | 3 | 2 | PM yazar → **insan onaylar** → QA otomatize eder | Spec ile test **aynı artefakt** olur. Drift'in fiziksel olarak zorlaştığı tek katman. |
| 2 | **Contract / şema** (OpenAPI, JSON Schema, event schema, Pact/CDC) | 5 | 2 | 2 | Tech Lead | Multi-agent'ta ajanlar paralel çalışıyor; desync buradan patlar. Şema spec'ten üretilebildiği için ROI en yüksek kalem. **Ama çakışmayı önlemez, yalnız yakalar** → [`03`](03-concurrency.md). |
| 3 | **Statik kapılar** (strict tip, lint, derleme, format, dead-code, dependency policy) | 4 | 1 | 1 | Tech Lead | Spec oracle'ı değil ama ajanın en sık hata sınıfını milisaniyede yakalar. Pazarlıksız zemin. |
| 4 | **Architecture fitness functions** (katman kuralları, import grafı, bağımlılık yönü) | 5 | 1 | 1 | Tech Lead | **v1.0'da eksikti.** Ajan tüm testleri geçerken mimariyi çürütebilir; bunu yakalayan tek çalıştırılabilir gate. Efor statik kapılar kadar düşük. Detay → [`04` §2](04-codebase-integrity.md). |
| 5 | **Integration / component** (Testcontainers, in-memory DB, gerçek widget ağacı) | 4 | 3 | 3 | Engineer | Gerçek hatalar dikişlerde yaşıyor. "Trophy" modelinin gövdesi. |
| 6 | **Regresyon / smoke çekirdeği** (kilitli, ajanın dokunamadığı set) | 4 | 2 | 2 | QA | Ajan-yazımı PR'ların red sebebi #1 CI kırılması. |
| 7 | **Security gate'leri** (SAST/Semgrep, secret scan, SCA+SBOM, authz contract: BOLA/BFLA) | 5\* | 2 | 2 | Security Engineer | \*Ayrı eksen: spec sadakatini değil, **spec'in sessizce ihlal ettiği kısıtları** yakalar. Ajanların auth sınırını bypass eden handler üretmesi ölçülmüş bir desen (arXiv 2605.30777). |
| 8 | **Property-based / invariant** (Hypothesis, fast-check, `glados`) | 4 | 3 | 2 | Engineer + Tech Lead | Örnek değil **kural** test eder. Ajanın uyduramayacağı testtir. ⚠ v1.0 bakımı "1" diyordu — gerçekçi değil: shrinking, seed yönetimi ve non-deterministik failure debug'ı gerçek maliyet. |
| 9 | **Incremental mutation** (değişen dosyalarda, PR gate) | 4 | 2 | 1 | Tech Lead / QA | *Testleri test eder.* "Sürekli yeşil" sahte testleri açığa çıkaran tek deterministik sinyal. PR başına yalnız diff'te koşar → gate olabilir. Tam suite haftalık trend için. |
| 10 | **E2E / kullanıcı yolculuğu** (Playwright, `integration_test`, PlayMode) | 4 | 4 | 4 | QA | Kullanıcının gördüğü gerçeği doğrulayan tek katman. Pahalı ve kırılgan → **5–10 kritik yolculukla sınırla**, asla kapsam aracı yapma. |
| 11 | **Golden / snapshot / deterministik replay** | 3 | 2 | 4 | Engineer / Designer | Deterministik replay (sabit seed + sabit timestep + kayıtlı input → final state hash) simülasyon/hesap zinciri içeren sistemlerde **en ucuz sadakat testi**. Screenshot golden'ları kolay kırılır; yalnız stabil bileşenlerde. |
| 12 | **Unit (saf domain mantığı)** | 3 | 2 | 2 | Engineer | Değerli ama abartılıyor. Ajan bunları bolca üretir → tam da bu yüzden **sadakat sinyali zayıf**. |
| 13 | **Performans / bütçe** (frame budget, bundle size, p95 latency, k6) | 2 | 3 | 2 | Engineer + Tech Lead | Spec'te "60 FPS" / "< 200 ms" yazıyorsa bu bir kabul kriteridir ve ölçülmelidir. |
| 14 | **Visual regression** (screenshot diff, design token diff) | 2 | 3 | 4 | Product Designer | Token diff (renk/spacing/tipografi sabitleri) screenshot diff'ten çok daha ucuz ve stabil — **önce onu kur**. |
| 15 | **Accessibility** (semantic label, kontrast, tap target) | 2 | 2 | 2 | Designer + QA | Store dağıtımı ve erişilebilirlik uyumu açısından anlamlı; lint benzeri kurallarla ucuz. |
| 16 | **Chaos / fault injection** | 1 | 4 | 3 | Tech Lead | Mobil + backend olgunlaştıktan sonra. Erken kurulursa efor/getiri oranı kötü. |
| 17 | **Keşifsel + LLM-as-judge review** | 3 | 1 | 5 | QA + PM + insan | Otomatikleştirilemeyen tek şey: **kullanım hissi** (etkileşim tepkisi, akıcılık, "doğru geliyor mu"). Hiçbir assert ile ölçülemez. Bilinçli olarak insana bırakılan alan. |

---

## 4. Spec gaming'e karşı 9 kontrol

Bu bölüm olmadan yukarıdaki her şey oyunlaştırılabilir.

### 4.1 Görev ayrımı (ZORUNLU, kapsamı sınırlı)

Testi yazan ajan ≠ kodu yazan ajan. Farklı context, farklı prompt, ideal olarak farklı model.

> **Kapsam (v1.0'daki belirsizlik giderildi):** Bu kural **yalnız** acceptance testleri, regresyon çekirdeği ve gizli set için geçerlidir. Engineer ajanı kendi unit / integration / property testlerini yazar — bu beklenen ve istenen davranıştır. Ayrımın amacı "ajan test yazmasın" değil, **ajanın geçmesi gereken sınavı kendisinin yazmasını engellemek**.

| Test kategorisi | Kod ajanı yazabilir mi? |
|---|---|
| Acceptance / BDD | ❌ |
| Regresyon çekirdeği | ❌ |
| Gizli set | ❌ (göremez) |
| Contract / şema | ❌ (Tech Lead ajanı) |
| Unit / integration / property | ✅ |

### 4.2 Kilitli test dosyaları (ZORUNLU)

`CODEOWNERS` + branch protection. `tests/acceptance/**`, `tests/regression/**`, `tests/hidden/**` ve `contracts/**` için Engineer ajanına **write yetkisi kapalı**. Değişiklik gerekiyorsa spec-change PR açar → [`06` §4](06-operations.md).

Şablon: [`templates/CODEOWNERS.example`](../templates/CODEOWNERS.example)

### 4.3 Gizli test seti (hidden split)

AC'lerin **%20–30'u** için testler ajanın göremediği bir konumda tutulur; yalnız merge queue içinde koşar.

Operasyonel gereklilikler — bunlar olmadan gizli set işe yaramaz:

1. **Ayrı konum.** Tercihen ayrı private repo veya ayrı bir CI secret'ıyla checkout edilen submodule. Aynı repoda "ajan bakmasın" temenniyle olmaz.
2. **Sızdırmayan failure raporu (ZORUNLU).** Gizli test kırıldığında CI çıktısı **assertion içeriğini, dosya adını, satır numarasını ve diff'i loglamaz.** Yalnız şunu yazar: `AC-042 gizli sette başarısız. İnsan incelemesi gerekiyor.` Aksi halde ajan log'dan testi tersine mühendislikle çıkarır ve overfit eder — gizli setin tüm amacı kaybolur.
3. **Manifest.** `tests/hidden/manifest.txt` yalnız AC ID listesi tutar (içerik yok). Criteria coverage checker bunu okur → §2.1.
4. **Ajan CI log erişimi kısıtı.** Ajan gizli-set job'unun ham log'una erişemez.
5. **Tahkim yolu.** Gizli test gerçekten hatalıysa hattı kilitlemesin → [`05` §4](05-roles.md).

⚠ **Kanıt notu:** Hidden split kod ajanları için henüz ölçülmemiştir; analog domain'de ölçülmüştür → [`01` §1.4](01-research.md). Pilotta ölçülecek kalem.

### 4.4 Mutation eşiği (ZORUNLU, incremental)

Kritik modüllerde **değişen dosyaların** mutation skoru < %80 → merge yok.

> **v1.0'daki çelişki düzeltilmiştir.** Önceki sürüm mutation'ı hem "haftalık koş" hem "merge gate" olarak tanımlıyordu; haftalık bir job merge'i gate'leyemez. Yeni model:
> - **PR başına:** yalnız diff'teki dosyalarda incremental mutation → **gate**, ~2–4 dk
> - **Haftalık:** kritik modüllerde tam suite → **trend metriği**, gate değil

"Coverage %95, mutation %30" tablosu sahte test suite'in imzasıdır.

### 4.5 Kırmızı kanıtı — CI üretir, ajan üretmez (ZORUNLU)

Testin implementasyondan **önce** kırmızı koştuğunun kanıtı gerekir.

> **v1.0'daki güvenlik açığı kapatılmıştır.** Önceki sürüm kırmızı log'unu *PR artefaktı* olarak istiyordu — yani ajanın ürettiği bir dosya. Ama bu repo'nun kendi kaynakçasındaki arXiv 2605.30777'nin baskın bulgu kategorilerinden biri **"fabricated success reports"**: ajanlar başarı raporu uyduruyor. **Ajanın ürettiği hiçbir log kanıt değildir.**

Doğru mekanizma: CI, PR'ı iki commit'e ayırır (test-only commit → impl commit), **test-only commit'i kendisi checkout eder, testi kendisi koşar** ve kırmızı olduğunu kendisi kaydeder. Ajan bu artefakta dokunamaz. Detay ve implementasyon → [`06` §2](06-operations.md).

### 4.6 Kriter izlenebilirliği (ZORUNLU)

Her test `AC-###` etiketi taşır. Etiketsiz AC → build kırmızı. Silinen test → hangi AC'yi öksüz bıraktığı raporlanır. Uygulayan: [`tools/criteria_coverage.py`](../tools/criteria_coverage.py).

Checker iki yönde de çalışır: testsiz AC **ve** var olmayan AC'ye referans veren test, ikisi de hata.

**Fixture istisnası.** Fixture/örnek kriter ID'si üreten dosyalar (meta-testler, checker'ın kendi testleri) `criteria-coverage:ignore-file` işareti taşır ve taranmaz; kapsadıkları gerçek AC yanlarındaki bir `.tags` dosyasından beyan edilir. İşaret **gate atlatmak için kullanılamaz**: yalnız referans *kaldırır*, kapsama *üretemez* — kötüye kullanımı build'i kırmızılaştırır, yeşillendirmez. Atlanan dosya sayısı her raporda görünür (sessiz istisna yok).

> **Tuzak:** Taranan bir dosyanın *yorumunda* bile var olmayan bir AC ID'si geçerse öksüz referans olarak raporlanır. Bu repo kurulurken iki kez yaşandı; `tests/acceptance/AC-001.tags` içinde kayıtlı.

### 4.7 Değişim kapsaması (change coverage) (ZORUNLU)

Toplam coverage değil, **diff'in** coverage'ı ≥ %85. Ajanın dokunduğu satır test edilmemişse geçmez.

### 4.8 Çapraz-model review (ZORUNLU)

Testleri ve implementasyonu **farklı model** review eder. AI-üretimi kodu aynı AI'nin review etmesindeki korelasyonlu hata desenini kıran ana mekanizma.

> **v1.0'da eksik olan tie-break kuralı:** İki model çelişirse *otomatik kazanan yoktur*. Karar sırası:
> 1. Çelişki **çalıştırılabilir bir iddiaysa** ("bu null olabilir") → iddiayı gösteren test yazılır. Test hakemdir.
> 2. Çelişki **stil/tasarım tercihiyse** → Tech Lead ajanının kararı, gerekçe PR'a yazılır.
> 3. Çelişki **spec yorumundaysa** → **insana** gider (G1 sahibi). Ajanlar arası oylama ile çözülmez.

### 4.9 Test değişikliği izolasyonu (ZORUNLU)

"Testi düzelttim" diyen hiçbir commit, üretim kodu değişikliğiyle **aynı PR'da** olamaz. Test değişikliği daima ayrı PR, daima gerekçeli, daima test sahibinin onayıyla.

---

## 5. Efor-düzeltilmiş kurulum sırası

Aynı liste **(Etki ÷ Toplam Efor)** ile sıralandı. Pilotta bu sıra izlenir.

| Sıra | Katman | Neden şimdi | Tahmini kurulum |
|:--:|---|---|---|
| 1 | Statik kapılar + derleme + dependency policy | Efor ~0, anında kazanç | 0.5 gün / repo |
| 2 | **Architecture fitness functions** | v1.0'da yoktu. Statik kapı kadar ucuz, contract kadar etkili. Drift'in ana panzehiri | 0.5–1 gün / repo |
| 3 | Contract / şema testleri | Paralel ajanların desync'i #1 hata kaynağı | 1–2 gün / servis sınırı |
| 4 | **Impact analysis skill dosyası** (hangi testi koş) | Dokümandaki **kanıtı en güçlü** müdahale: %70 regresyon düşüşü. `04` §5 | 0.5–1 gün / repo |
| 5 | Security gate'leri (secret + SAST + SCA) | Mevcut DevSecOps birikimiyle neredeyse hazır | 1 gün / pipeline |
| 6 | **Merge queue + worktree izolasyonu** | v1.0'da yoktu. Çakışmayı önleyen tek yapısal mekanizma. `03` | 0.5 gün / repo |
| 7 | Acceptance / BDD (yalnız kritik akışlar) + criteria coverage checker | Spec sadakatinin çekirdeği | 2–3 gün + AC başına ~20 dk |
| 8 | Regresyon smoke çekirdeği (kilitli) | Ajan-kaynaklı regresyonu durdurur | 1 gün |
| 9 | Property-based (para/kota/state machine/invariant) | Efora göre en yüksek mutation kazancı | 0.5 gün saf fonksiyon · 1–2 gün state machine modeli |
| 10 | Integration (yalnız dikişler) | Trophy gövdesi | Sürekli, feature başına |
| 11 | Deterministik replay (simülasyon/hesap zinciri) | Çok ucuz sadakat | 1–2 gün, sonrası bedava |
| 12 | Incremental mutation (PR gate) | Test kalitesinin tek dürüst metriği | 1 gün kurulum |
| 13 | Duplikasyon + API surface diff | Çürümenin ikinci ekseni. `04` §3–4 | 0.5 gün |
| 14 | Gizli set + sızdırmayan raporlama | Overfit kırıcı | 1 gün |
| 15 | E2E kritik yolculuklar (max 10) | Kullanıcı gerçeği | 3–5 gün |
| 16 | Unit (saf logic) | Ajan zaten üretiyor; kural yaz, kota koyma | Sürekli |
| 17 | Perf / frame bütçesi | Gerçek zamanlı render eden sistemlerde erken, diğerlerinde sonra | 1–2 gün |
| 18 | Design token diff | Screenshot diff'ten önce | 1 gün |
| 19 | A11y lint | Store öncesi | 0.5 gün |
| 20 | Visual regression (screenshot) | Ancak UI stabilize olunca | 2–3 gün |
| 21 | Chaos / fault injection | v2 konusu | — |

**Kabaca:** Sıra 1–8, toplam eforun ~%25'i ve sadakat + çakışma kazancının ~%75'i. Pilotta buraya kadar git, gerisini kanıt geldikçe aç.
