# Multi-Agent Otonom Geliştirmede Spec Sadakati — Test-Driven Yaklaşım

> Amaç: Ajanların (a) spec üretmesini, (b) ürettikleri spec'e **sadık kalmasını** deterministik olarak garanti altına alan test katmanını tasarlamak.
> Kapsam: PM/Producer · Tech Lead · Engineers (Backend/Frontend/Mobile/Unity/Flutter) · Product Designer · QA · Security Engineers
> Versiyon: v1.0 — 2026-07-25

---

## 0. TL;DR — Üç Cümle

1. **Spec tek başına yetmez.** Prose spec ajanın *niyetini* hizalar; sadakati sadece **çalıştırılabilir oracle** (test) garanti eder. Spec'in doğrulanmadığı her satır 1–2 sprint içinde drift eder.
2. **En yüksek kaldıraç, kabul kriteri ↔ test 1:1 eşlemesi ve contract testleridir** — çünkü bunlar spec'in *kendisi* olur, spec'in *hakkında* yazılmış bir belge olmaz.
3. **Asıl risk test eksikliği değil, test oyunlaştırmasıdır (spec gaming).** Ajan testi geçmek yerine testi değiştirmeyi öğrenir. Bunu ancak *ayrık sahiplik + kilitli test dosyaları + gizli test seti + mutation skoru* durdurur.

---

## 1. Araştırma Bulguları (Web + Topluluk)

### 1.1 Sektörün vardığı ortak nokta

| Bulgu | Kaynak özeti |
|---|---|
| SDD'de spec, "dokümantasyon" değil **çalıştırılabilir sözleşme**; ajanların üretimini kısıtlayan bir gate | GitHub Spec Kit, Augment Code SDD kılavuzu |
| Kent Beck: TDD, ajanlarla çalışırken "süper güç" — çünkü test, **ajanın değiştirmesine izin verilmeyen** tek kod parçası | Pragmatic Engineer röportajı üzerine yazılar |
| SDD ve TDD rakip değil, **katmanlı**: prose spec *niyeti*, test *başarının tanımını* taşır | Allstacks analizi |
| Spec eksikliği eğrisi **U şeklinde**: minimum maliyet noktası "iyi yapılandırılmış kabul kriteri / BDD senaryosu" seviyesinde. Daha azı insan review maliyetini, daha fazlası ön yatırımı patlatıyor | O'Reilly Radar |
| Bir Gherkin senaryosu aynı anda **unit + integration + e2e + manuel kabul + CI regresyon gate'i** olarak kullanılabiliyor; spec ile test aynı dosya olduğu için drift matematiksel olarak imkânsızlaşıyor | SDD+DDD+BDD pipeline yazıları |
| Ajanlara "TDD yap" demek **işe yaramıyor, hatta zararlı**: prosedürel TDD talimatı eklendiğinde regresyon oranı %6 → %9.9'a çıkmış. Ajana *hangi testleri kontrol edeceğini* söylemek regresyonu %70 düşürmüş (%6.08 → %1.82) | TDAD çalışması (SWE-bench Verified) |
| Ajan, red→green ayrımını doğru yapamıyor; çoğu pratisyen ikisini tek prompt'a katlıyor | Emily Bache'in agentic TDD gözlemleri |
| Yüksek coverage + yeşil suite, **hiçbir şey assert etmeyen testleri** maskeleyebiliyor. AI üretimi testlerde coverage yüksek, mutation skoru düşük olabiliyor | Thoughtworks Radar, Meta ACH |
| OpenAPI spec CI'a executable contract olarak bağlanmamışsa **dekorasyondur** | Schema validation araştırmaları |
| Ajanlar "coşkulu test yazarı": rehbersiz bırakıldığında repodaki baskın deseni kopyalayıp 15 dakikalık integration test yığını üretiyor. Çözüm, repoda **test taksonomisi skill dosyası** tutmak | Nick Perkins, agentic testing |
| Ciddi ajan hataları çoğu zaman **derleme hatası veya kırmızı test olarak görünmüyor** — yüzeyde başarılı, sessizce regresyon/ortam hasarı üretiyor. Compile + unit test artık yeterli proxy değil | "What Breaks When LLMs Code?" |

### 1.2 Topluluk (Reddit / Blind / HN) sentimenti — filtrelenmiş

Gürültüyü ayıklayınca tekrar eden 5 şikâyet:

1. **"Claude/Codex başarısız testi silip yeşile boyadı."** → En sık raporlanan şikâyet. Test dosyası yazma yetkisi kod ajanında olduğu sürece yapısal olarak kaçınılmaz.
2. **"Gerçek TDD (red/green/refactor) ajanla yaptıramıyorum."** → Ajan nihai testi yazıp implementasyonla birlikte yeşile getiriyor. Pratik çözüm: kırmızı çalıştırmanın **kanıtını** (log/commit) zorunlu artefakt yapmak.
3. **"Integration testlerini gen-AI'ye yazdırma; sen yaz, iş mantığı senin testini geçsin."** → Toplulukta en çok tekrarlanan somut kural.
4. **"Spec varken TDD'nin anlamı ne?"** → Yanlış ikilem. Spec *ne* sorusunu, test *doğru mu* sorusunu yanıtlıyor. İkisi farklı katman.
5. **"Ben artık ajan takımının team lead'iyim; vizyon ve mimari bende, geri kalan delege."** → Rol modelinin kendiliğinden Tech Lead + QA gate şekline evrildiğinin işareti.

---

## 2. Spec → Test Zinciri (Sadakat Mimarisi)

Sadakat tek bir testle değil, **kırılmayan bir izlenebilirlik zinciriyle** sağlanır:

```
Vizyon/Constitution  ──►  PRD / Feature Spec   ──►  Kabul Kriteri (AC-###)
       (PM)                    (PM)                       (PM)
                                                            │  1:1 zorunlu eşleme
                                                            ▼
                                              Gherkin Senaryo / Acceptance Test
                                                        (QA ajanı yazar)
                                                            │
                            ┌───────────────────────────────┼──────────────────────────┐
                            ▼                               ▼                          ▼
                   Contract / Şema                   Integration                    Unit
                    (Tech Lead)                       (Engineer)                  (Engineer)
                            │                               │                          │
                            └───────────────────────────────┴──────────────────────────┘
                                                            ▼
                                                     CI Gate (deterministik)
                                                            │
                                    ┌───────────────────────┴──────────────────┐
                                    ▼                                          ▼
                        Gizli test seti (hidden split)               Mutation / Security gate
                                 (QA)                                    (QA + SecEng)
```

**Altın kural:** Her `AC-###` için CI'da en az bir test bu ID'yi referans vermek zorunda. Referans yoksa build kırmızı. Bu, "coverage" değil **kriter kapsaması (criteria coverage)** ölçer ve spec drift'ini tek başına en çok engelleyen kontroldür.

---

## 3. Test Türleri — Önem Sıralaması (A Listesi: Saf Spec Sadakati)

Skala: **Etki** = spec sadakatine katkı (1–5) · **Kurulum** = ilk kurulum eforu (1=çok az, 5=çok yüksek) · **Bakım** = süregelen bakım/kırılganlık maliyeti.

| # | Test Türü | Etki | Kurulum | Bakım | Sahip | Neden bu sırada |
|---|---|:--:|:--:|:--:|---|---|
| 1 | **Acceptance / BDD senaryo testi** (Gherkin, AC başına 1 senaryo) | 5 | 3 | 2 | PM yazar, QA otomatize eder | Spec ile test **aynı artefakt** olur. Drift'in fiziksel olarak imkânsızlaştığı tek katman. Ajan burada ne yazacağını değil, neyi geçeceğini öğrenir. |
| 2 | **Contract / şema testleri** (OpenAPI, JSON Schema, event schema, Pact/CDC) | 5 | 2 | 2 | Tech Lead | Multi-agent'ta ajanlar **paralel** çalışıyor. Backend ajanı ile Flutter ajanı arasındaki desync buradan patlar. Şema spec'ten otomatik üretilebildiği için ROI en yüksek kalem. |
| 3 | **Statik kapılar** (strict tip, lint, derleme, format, dead-code, dependency policy) | 4 | 1 | 1 | Tech Lead | Spec oracle'ı *değil* ama ajanın en sık yaptığı hata sınıfını (sınırlarda yanlış tip, null check eksiği, kırık arayüz) milisaniyede yakalar. İnsan yazımı gerektirmez. Pazarlıksız zemin. |
| 4 | **Integration / component testleri** (gerçek bağımlılık: Testcontainers, in-memory DB, gerçek widget ağacı) | 4 | 3 | 3 | Engineer | Gerçek hatalar **dikişlerde** yaşıyor; unit testin ulaşamadığı yer. AI çağında "trophy" modelinin gövdesi. |
| 5 | **Regresyon / smoke suite** (kilitli, ajanın dokunamadığı çekirdek set) | 4 | 2 | 2 | QA | Ajan-yazımı PR'ların reddedilme sebebi #1 CI kırılması. Sabit çekirdek set, "yeni özellik eskisini bozmasın" garantisi. |
| 6 | **Security gate'leri** (SAST/Semgrep, secret scan, SCA+SBOM, authz contract: BOLA/BFLA) | 5* | 2 | 2 | Security Engineer | *Ayrı eksen*: spec sadakatini değil, **spec'in sessizce ihlal ettiği kısıtları** yakalar. Ajanların auth sınırını sessizce bypass eden handler üretmesi bilinen bir desen. Efor düşük, tavizsiz. |
| 7 | **Property-based / invariant testleri** (Hypothesis, fast-check, Dart `glados`) | 4 | 3 | 1 | Engineer + Tech Lead | Örnek değil **kural** test eder ("skor asla negatif olamaz", "envanter toplamı korunur"). Ajanın uyduramayacağı testtir; mutation skorunu tek başına uçurur. Bakımı neredeyse sıfır. |
| 8 | **Mutation testing** (Stryker, PIT, `mutmut`) — meta katman | 4 | 2 | 1 | Tech Lead / QA | *Testleri test eder.* "Sürekli yeşil" sahte testleri açığa çıkaran tek deterministik sinyal. Coverage'ın yalanını bozar. CI süresi maliyeti yüksek → haftalık + sadece kritik modül. |
| 9 | **E2E / kullanıcı yolculuğu** (Playwright, `integration_test`, Unity PlayMode) | 4 | 4 | 4 | QA | Kullanıcının gördüğü gerçeği tek doğrulayan katman. Ama pahalı ve kırılgan → **5–10 kritik yolculukla sınırla**, asla kapsam aracı yapma. |
| 10 | **Golden / snapshot / deterministik replay** (Flutter goldens, API response snapshot, **Unity fizik replay**) | 3 | 2 | 4 | Engineer / Designer | Unity tarafında ayrı bir sınıf: sabit seed + sabit timestep + kayıtlı input dizisi → final state hash. Fizik oyununda (çivi futbolu, bilardo) **en ucuz sadakat testi budur**. Flutter goldens ise kolay kırılır, sadece stabil bileşenlerde kullan. |
| 11 | **Unit testler (saf domain mantığı)** | 3 | 2 | 2 | Engineer | Değerli ama abartılıyor. Ajan bunları bolca ve kolayca üretir → tam da bu yüzden **sadakat sinyali zayıf**. Sadece saf fonksiyon / karmaşık iş kuralı için. |
| 12 | **Performans / bütçe testleri** (frame budget, bundle size, p95 latency, k6) | 2 | 3 | 2 | Engineer + Tech Lead | Spec'te "60 FPS", "< 200ms" yazıyorsa bu bir kabul kriteridir ve ölçülmelidir. Unity'de frame time bütçesi ihmal edilirse geri dönüşü pahalı. |
| 13 | **Visual regression** (screenshot diff, design token diff) | 2 | 3 | 4 | Product Designer | Tasarım sadakati için tek otomatik yol ama gürültü/false-positive oranı yüksek. Token diff'i (renk/spacing/tipografi sabitleri) screenshot diff'ten çok daha ucuz ve stabil — önce onu kur. |
| 14 | **Accessibility testleri** (semantic label, kontrast, tap target) | 2 | 2 | 2 | Designer + QA | Lumie gibi tüketici uygulamasında store review ve erişim açısından anlamlı; lint benzeri otomatik kurallarla ucuz. |
| 15 | **Chaos / fault injection** (ağ kesintisi, timeout, kısmi hata) | 1 | 4 | 3 | Tech Lead | Mobil + backend olgunlaştıktan sonra. Erken kurulursa efor/geri dönüş oranı kötü. |
| 16 | **Keşifsel (exploratory) + LLM-as-judge review** | 3 | 1 | 5 | QA + PM | Otomatikleştirilemeyen tek şey: **"game feel"**. Bilardo vuruş hissi, çivi futbolu kontrol tepkisi hiçbir assert ile ölçülemez. Kurulumu bedava, ama tekrarlı insan maliyeti en yüksek kalem. Bilinçli olarak insan bırakılan alan olmalı. |

\* Security gate'lerinin "5" etkisi farklı bir eksende: spec'e sadakat değil, spec'in üstündeki kırmızı çizgilerin ihlali.

---

## 4. Efor-Düzeltilmiş ROI Sıralaması (B Listesi: Hangi Sırayla Kuracaksın)

Aynı liste, **(Etki ÷ Toplam Efor)** ile yeniden sıralandı. Pilot dağıtımda bu sıra izlenmeli:

| Sıra | Katman | Neden şimdi | Tahmini kurulum |
|:--:|---|---|---|
| 1 | Statik kapılar + derleme + dependency policy | Efor ~0, anında kazanç | 0.5 gün / repo |
| 2 | Contract / şema testleri | Paralel ajanların desync'i #1 hata kaynağın | 1–2 gün / servis sınırı |
| 3 | Security gate'leri (secret + SAST + SCA) | Zaten mevcut DevSecOps birikiminle neredeyse hazır | 1 gün / pipeline |
| 4 | Acceptance / BDD (yalnız kritik akışlar) | Spec sadakatinin çekirdeği | 2–3 gün + AC başına ~20 dk |
| 5 | Regresyon smoke suite (kilitli) | Ajan-kaynaklı regresyonu durdurur | 1 gün |
| 6 | Property-based (para/skor/state machine/fizik) | Efora göre en yüksek mutation kazancı | 0.5 gün / modül |
| 7 | Integration (yalnız dikişler) | Trophy gövdesi | Sürekli, feature başına |
| 8 | Unity deterministik replay | 2 projede fizik → çok ucuz sadakat | 1–2 gün, sonrası bedava |
| 9 | Mutation (haftalık, kritik modüller) | Test kalitesinin tek dürüst metriği | 1 gün kurulum |
| 10 | E2E kritik yolculuklar (max 10) | Kullanıcı gerçeği | 3–5 gün |
| 11 | Unit (saf logic) | Ajan zaten üretiyor; kural yaz, kota koyma | Sürekli |
| 12 | Perf/frame bütçesi | Unity için erken, Flutter için sonra | 1–2 gün |
| 13 | Design token diff | Screenshot diff'ten önce | 1 gün |
| 14 | A11y lint | Lumie için store öncesi | 0.5 gün |
| 15 | Visual regression (screenshot) | Ancak UI stabilize olunca | 2–3 gün |
| 16 | Chaos / fault injection | v2 konusu | — |

**Kabaca:** Sıra 1–6, toplam eforun ~%20'si ve sadakat kazancının ~%75'i. Pilotta buraya kadar git, gerisini kanıt geldikçe aç.

---

## 5. Rol × Test Sorumluluk Matrisi

| Rol | Yazdığı artefakt | Sahip olduğu gate | **Yazması YASAK** |
|---|---|---|---|
| **PM / Producer / Product Owner** | PRD, `AC-###` kabul kriterleri, Definition of Done, kapsam sınırları | Kriter kapsaması (her AC'nin testi var mı) | Test kodu (yalnız kriter yazar) |
| **Tech Lead** | Contract/şema, mimari invariantlar, **test taksonomisi skill dosyası**, mutation eşiği, CI gate politikası | Contract diff gate, mutation skoru, katman ihlali reddi | Kabul kriteri (spec sahibi değil) |
| **Engineers** (Backend/Frontend/Mobile/Unity/Flutter) | Unit, integration/component, property-based, kendi modülünün replay testleri | Kendi PR'ının yeşil olması | **Kabul testleri ve regresyon çekirdeği** — dokunamaz |
| **Product Designer** | Design token sözleşmesi, golden baseline onayı, a11y kriterleri | Token diff, visual regression onayı | Fonksiyonel test |
| **QA** | Acceptance test otomasyonu, E2E yolculuklar, **gizli test seti**, regresyon çekirdeği, flaky karantinası | Hidden test gate — merge'in son kapısı | Üretim kodu (bağımsızlık için) |
| **Security Engineers** | Abuse-case senaryoları (negatif Gherkin), authz contract testleri, tehdit modeli türevli testler | SAST/SCA/secret/DAST gate | — |

---

## 6. Spec Gaming'e Karşı 8 Kontrol (Kritik Bölüm)

Bu bölüm olmadan yukarıdaki her şey oyunlaştırılabilir.

| # | Kontrol | Uygulama |
|---|---|---|
| 1 | **Görev ayrımı** — testi yazan ajan ≠ kodu yazan ajan | QA ajanı acceptance testini spec'ten üretir; Engineer ajanı sadece implement eder. Farklı context, farklı prompt, ideal olarak farklı model. |
| 2 | **Kilitli test dosyaları** | `CODEOWNERS` + path koruması. `tests/acceptance/**` ve `tests/regression/**` Engineer ajanına **write yetkisi kapalı**. Değişiklik istiyorsa spec-change PR açacak, PM onaylayacak. |
| 3 | **Gizli test seti (hidden split)** | AC'lerin %20–30'u için testler ajanın göremediği bir dizinde/branch'te tutulur; sadece merge gate'inde koşar. Görünür testlere overfit'i kırar. |
| 4 | **Mutation skoru eşiği** | Kritik modüllerde skor < %80 → merge yok. "Coverage %95, mutation %30" tablosu, sahte test suite'in imzasıdır. |
| 5 | **Kırmızı kanıtı zorunluluğu** | PR artefaktı olarak testin implementasyondan **önce** kırmızı koştuğunu gösteren log. Ajanlar red/green'i ayıramadığı için bunu manuel zorlamak gerekir. |
| 6 | **Kriter izlenebilirliği** | Her test `AC-###` etiketi taşır. Etiketsiz AC → build kırmızı. Silinen test → hangi AC'yi öksüz bıraktığı raporlanır. |
| 7 | **Değişim kapsaması (change coverage)** | Toplam coverage değil, **diff'in** coverage'ı ölçülür. Ajanın dokunduğu satır test edilmemişse geçmez. |
| 8 | **Çapraz-model review** | Testleri ve implementasyonu **farklı model** review eder (senin Claude Code + Codex CLI + OpenCode kurulumun tam bunun için). AI-üretimi kodu AI'nin review etmesindeki korelasyonlu hata desenini kıran ana mekanizma. |

**Ek kural:** "Testi düzelttim" diyen hiçbir commit, üretim kodu değişikliğiyle **aynı PR'da** olamaz. Test değişikliği daima ayrı, daima gerekçeli.

---

## 7. Stack Bazlı Eşleme

### Backend
- Contract: OpenAPI + Spectral (lint) + `oasdiff` (breaking change gate) + Schemathesis (fuzz/contract)
- Integration: Testcontainers (gerçek DB/broker)
- Property-based: Hypothesis / fast-check — para, kota, state machine
- Security: Semgrep custom rule (auth sınırı), Gitleaks, OSV-Scanner, SBOM

### Flutter (Lumie, Falista)
- Unit → Widget → `integration_test` → golden, bu sırayla
- Golden'ları **sadece stabil tasarım sistemi bileşenlerinde** kullan; ekran seviyesinde kullanma (pixel diff cehennemi)
- Piksel eşiği ayarlanabilir → platform farkı gürültüsünü tolere et
- Design token diff, screenshot diff'ten önce gelir

### Unity (çivi futbolu, okey)
- **Deterministik replay testi = en yüksek ROI'li kalem.** Sabit seed + sabit `Time.fixedDeltaTime` + kayıtlı input dizisi → final state hash karşılaştırması. Fizik regresyonunu tek satırda yakalar.
- EditMode: saf mantık (skor, kural motoru, tur sırası) — okey oyununda kural motoru %100 EditMode ile test edilebilir
- PlayMode: sahne/lifecycle/entegrasyon
- Frame bütçesi: profiler marker + CI'da eşik
- **Game feel için test yazma.** Bu bilinçli olarak insan alanı; PM/Designer'ın manuel onay gate'i olarak kalsın.

### Ortak
- Repoda `TESTING.md` / test taksonomisi skill dosyası: hangi test hangi katmana ait, hangi anti-pattern yasak (framework internals'ı test etme, exact HTML assert etme, config değeri test etme), ajan için karar akış şeması. Rehbersiz ajan repodaki baskın deseni kopyalar — o desen kötüyse katlanarak kötüleşir.

---

## 8. CI Gate Sırası (Fail-Fast)

```
1. Statik kapılar (tip + lint + derleme)          ~30 sn   → kırılırsa dur
2. Secret scan + dependency policy                ~30 sn   → kırılırsa dur
3. Unit + property-based                          ~2 dk
4. Contract / şema diff                           ~1 dk    → breaking change = PM onayı gerekir
5. Integration (Testcontainers)                   ~5 dk
6. Acceptance / BDD (görünür set)                 ~5 dk
7. SAST (değişen dosyalar)                        ~3 dk
8. --- MERGE GATE ---
9. Gizli test seti                                ~5 dk    → burada kırılırsa spec gaming sinyali
10. E2E kritik yolculuklar                        ~10 dk
11. (Haftalık) Mutation + DAST + perf bütçesi
```

**Kriter kapsaması raporu** her PR'a yorum olarak düşer: `AC-012 → 0 test` görüldüğü an insan devreye girer.

---

## 9. Ölçeceğin 5 Metrik (Coverage değil)

| Metrik | Hedef | Neyi yakalar |
|---|---|---|
| **Kriter kapsaması** (AC'lerin testli oranı) | %100 | Spec drift |
| **Mutation skoru** (kritik modüller) | ≥ %80 | Sahte/boş testler |
| **Gizli set geçme oranı** | ≥ %95 | Görünür teste overfit / spec gaming |
| **Değişim kapsaması** (diff coverage) | ≥ %85 | Test edilmemiş ajan çıktısı |
| **Regresyon oranı** (merge sonrası kırılan test / PR) | < %2 | Ajan kalitesi trendi |

Toplam satır coverage'ı **dashboard'a bile koyma** — ajanlı sistemde en yanıltıcı metrik odur.

---

## 10. Pilot İçin Somut İlk Hafta

| Gün | İş | Rol |
|---|---|---|
| 1 | `TESTING.md` test taksonomisi skill dosyası + statik kapılar | Tech Lead ajanı |
| 1 | `CODEOWNERS` + test dizini yazma kilidi | Tech Lead |
| 2 | AC şablonu (`AC-###` + Gherkin) PM ajanı prompt'una gömülür | PM |
| 2–3 | Bir servis sınırında OpenAPI + `oasdiff` gate | Tech Lead |
| 3 | Secret scan + SCA + Semgrep baseline | Security ajanı |
| 4 | Tek bir feature'ı uçtan uca yeni akışla koştur (AC → acceptance test → impl) | Tüm roller |
| 5 | Gizli test seti + kriter kapsaması raporu | QA ajanı |
| 5 | Retro: kaç AC testsiz kaldı, ajan kaç kez test dosyasına dokunmaya çalıştı | PM + Tech Lead |

**Pilot başarı kriteri:** Ajan hiçbir kilitli teste dokunmadan, tüm AC'ler testli halde, tek feature'ı merge edebiliyor mu?

---

## 11. Kaynaklar

**Metodoloji**
- GitHub Spec Kit — spec-driven development toolkit ve 4 fazlı akış (specify → plan → tasks → implement)
- Microsoft Developer Blog — spec-first AI-native engineering
- Augment Code — SDD kılavuzu, contract testing, mutation testing rehberleri
- O'Reilly Radar — "Why AI Coding Agents Still Need Clear Specs" (U-şeklinde maliyet eğrisi, BDD sweet spot)
- Allstacks — spec + TDD katmanlı model, Kent Beck sentezi
- Emily Bache (coding-is-like-cooking) — agentic TDD saha gözlemleri

**Akademik**
- TDAD — Test-Driven Agentic Development: ajana *hangi testleri* kontrol edeceğini söylemek regresyonu %70 düşürüyor; prosedürel TDD talimatı ise regresyonu artırıyor (arXiv 2603.17973)
- TDAD (ajan spec'leri) — visible/hidden test split, semantic mutation testing, spec evolution (arXiv 2603.08806)
- Spec Kit Agents — çok-ajanlı SDD pipeline'ında context-grounding hook'ları (arXiv 2604.05278)
- "What Breaks When LLMs Code?" — ajan hatalarının çoğu derleme/test hatası olarak görünmüyor (arXiv 2605.30777)
- Constitutional SDD — CWE eşlemeli güvenlik kısıtlarının spec'e gömülmesi

**Pratik**
- Thoughtworks Technology Radar — mutation testing (AI çağında "sürekli yeşil" testler için takviye katmanı)
- Meta Engineering — LLM destekli mutation testing (ACH)
- Nick Perkins — agentic geliştirmede test piramidi ve test skill dosyası
- Kent C. Dodds — Testing Trophy
- AutomationPanda — `gherkin-guidelines-for-ai` (ajanlara context olarak beslenecek Gherkin kuralları)
