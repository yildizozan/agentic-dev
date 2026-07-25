# 01 — Araştırma Bulguları ve Kaynaklar

> Bu dosya **tanımlayıcı** (descriptive), normatif değil. Buradaki bulgular `02`–`08` dosyalarındaki kuralların gerekçesidir.
> Kural arıyorsan `02`+ dosyalarına git.

---

## 1.1 Sektörün vardığı ortak nokta

| Bulgu | Kaynak | Kanıt gücü |
|---|---|---|
| SDD araçları spec'i yalnız dokümantasyon değil, üretimi yönlendiren ve bazı iddiaları gate'e bağlayan sözleşme olarak kullanıyor | GitHub Spec Kit, Augment Code SDD kılavuzu | Pratik / araç |
| Kent Beck: TDD, ajanlarla çalışırken "süper güç" — çünkü test, **ajanın değiştirmesine izin verilmeyen** tek kod parçası | Pragmatic Engineer röportajı üzerine yazılar | Uzman görüşü |
| SDD ve TDD rakip değil, **katmanlı**: prose spec *niyeti*, test *başarının tanımını* taşır | Allstacks analizi | Analiz |
| Spec eksikliği eğrisi **U şeklinde**: minimum maliyet noktası "iyi yapılandırılmış kabul kriteri / BDD senaryosu" seviyesinde | O'Reilly Radar | Analiz |
| Bir Gherkin senaryosu aynı anda unit + integration + e2e + manuel kabul + CI regresyon gate'i olarak kullanılabiliyor; spec ile test aynı dosya olduğu için drift zorlaşıyor | SDD+DDD+BDD pipeline yazıları | Pratik |
| **Ajana *hangi testleri* kontrol edeceğini söylemek regresyonu %70 düşürüyor** (%6.08 → %1.82). Prosedürel "TDD yap" talimatı ise regresyonu **artırıyor** (%6.08 → %9.94) | TDAD, arXiv 2603.17973 | **Ölçüm (deneysel)** ⚠ bkz. 1.3 |
| Ajan, red→green ayrımını doğru yapamıyor; çoğu pratisyen ikisini tek prompt'a katlıyor | Emily Bache, agentic TDD gözlemleri | Saha gözlemi |
| Yüksek coverage + yeşil suite, **hiçbir şey assert etmeyen testleri** maskeleyebiliyor. AI üretimi testlerde coverage yüksek, mutation skoru düşük olabiliyor | Thoughtworks Radar, Meta ACH | Pratik / endüstri |
| OpenAPI spec CI'a executable contract olarak bağlanmamışsa **dekorasyondur** | Schema validation araştırmaları | Pratik |
| Ajanlar "coşkulu test yazarı": rehbersiz bırakıldığında repodaki baskın deseni kopyalayıp 15 dakikalık integration test yığını üretiyor. Çözüm: repoda **test taksonomisi skill dosyası** | Nick Perkins, agentic testing | Saha gözlemi |
| Ciddi ajan hataları çoğu zaman **derleme hatası veya kırmızı test olarak görünmüyor**. Baskın kategoriler: constraint violation, **destructive operations**, authorization bypass, **deception / fabricated success reports**. 547 gerçek olay, 326'sı high/critical | "What Breaks When LLMs Code?", arXiv 2605.30777 | **Ölçüm (ampirik tarama)** |
| Hidden split + semantic mutation + spec-evolution regresyonu, tool-using agent tanımı domain'inde birlikte değerlendirilmiş bir yaklaşım | "Test-Driven AI Agent Definition", arXiv 2603.08806 | **Ölçüm (analog domain)** ⚠ bkz. 1.4 |

---

## 1.2 Topluluk sentimenti (filtrelenmiş)

Gürültü ayıklandığında tekrar eden 5 şikâyet:

1. **"Ajan başarısız testi silip yeşile boyadı."** → Tekrarlanan şikâyetlerden
   biri. Kod ve kritik oracle aynı kimlik/yetki alanındaysa teşvik çatışması
   oluşur. → Karşılık: [`02` §4.2 kilitli test dosyaları](02-spec-fidelity.md).
2. **"Gerçek TDD (red/green/refactor) ajanla yaptıramıyorum."** → Ajan nihai testi yazıp implementasyonla birlikte yeşile getiriyor. → Karşılık: [`06` §2 CI-üretimli kırmızı kanıtı](06-operations.md).
3. **"Integration testlerini gen-AI'ye yazdırma; sen yaz, iş mantığı senin testini geçsin."** → Toplulukta en çok tekrarlanan somut kural. → Karşılık: [`05` rol matrisi](05-roles.md).
4. **"Spec varken TDD'nin anlamı ne?"** → Yanlış ikilem. Spec *ne* sorusunu, test *doğru mu* sorusunu yanıtlıyor.
5. **"Ben artık ajan takımının team lead'iyim."** → Rol modelinin kendiliğinden Tech Lead + QA gate şekline evrildiğinin işareti.

---

## 1.3 ⚠ TDAD bulgusunun geçerlilik sınırı (önemli kayıt)

Bu doküman ailesindeki en yüksek kanıtlı bulgu TDAD'dan geliyor, ama **transfer edilebilirliği sınırlı** ve bunu açıkça kaydetmek gerekiyor:

| Boyut | Çalışmadaki değer |
|---|---|
| Modeller | Qwen3-Coder 30B (100 instance), Qwen3.5-35B-A3B (25 instance) — **küçük, açık-ağırlık** |
| Donanım | Consumer hardware |
| Benchmark | SWE-bench Verified |
| Yazarların yorumu | *"smaller models benefit more from contextual information (which tests to verify) than from procedural instructions (how to do TDD)"* |

**Sonuç:** "Ajanlara TDD yap demek zararlıdır" **frontier modeller için kanıtlanmış değildir.** Claude/Codex sınıfı modellerde prosedürel TDD talimatının etkisi ölçülmemiştir.

Bu repoda buna göre davranıyoruz:
- **Benimsiyoruz:** impact analysis / "hangi testleri koş" mekanizması — mekanizma model-bağımsız mantıklı ve ölçülmüş. → [`04` §5](04-codebase-integrity.md)
- **Benimsemiyoruz:** "ajana TDD anlatma" yasağı. Bunun yerine prosedürü *insan/CI tarafına* alıyoruz (kırmızı kanıtı CI üretir), ajana anlatmayı yasaklamıyoruz.
- **Ölçmemiz gerekiyor:** pilotta kendi modellerimizle regresyon oranı. Hedef metrik → [`07`](07-metrics.md).

---

## 1.4 ⚠ İki farklı "TDAD" — karıştırılmamalı

Kaynakçada aynı kısaltmayla **iki ayrı paper** var. Erken taslaklarda birbirine karıştıysa düzeltilmiştir:

| | arXiv 2603.17973 | arXiv 2603.08806 |
|---|---|---|
| Açılım | Test-Driven Agentic **Development** | Test-Driven AI Agent **Definition** |
| Konu | Kod ajanının **ürettiği koddaki** regresyon | **Ajanın kendisini** (prompt/tool-using agent) spec'ten derlemek |
| Mekanizma | AST tabanlı kod–test grafı, impact analysis | Behavioral spec → test, ikinci ajan prompt'u testler geçene kadar iyileştirir |
| Hidden split neyi ölçüyor | — | **Prompt** optimizasyonunun görünür testlere overfit'i |
| Mutation neyi mutasyona uğratıyor | — | **Prompt varyantları**, kod değil |

**Bunun pratik sonucu:** `02` §4.3'teki hidden test seti ve §4.4'teki mutation eşiği, 2603.08806'dan **doğrudan kanıt almıyor** — oradaki mekanizmalar analog bir domain'de (ajan derlemesi) ölçülmüş. Kod ajanları için bunlar **gerekçeli ama henüz ölçülmemiş** kontroller. Pilotta kendi verimizi üretmemiz gereken kalemler bunlar.

---

## 1.5 Kaynaklar

Doğrulama durumu açıkça işaretlidir. `✅` = URL ve içerik bu repo yazılırken doğrulandı. `⚠` = kaynak gerçek ama kalıcı URL doğrulanmadı, kendin ara.

### Akademik

| Kaynak | Durum |
|---|---|
| TDAD: Test-Driven Agentic Development — Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis — [arxiv.org/abs/2603.17973](https://arxiv.org/abs/2603.17973) · [PDF](https://arxiv.org/pdf/2603.17973) · [ResearchGate](https://www.researchgate.net/publication/402739199_TDAD_Test-Driven_Agentic_Development_-_Reducing_Code_Regressions_in_AI_Coding_Agents_via_Graph-Based_Impact_Analysis) | ✅ |
| Test-Driven AI Agent Definition — Compiling Tool-Using Agents from Behavioral Specifications — [arxiv.org/abs/2603.08806](https://arxiv.org/abs/2603.08806) | ✅ |
| What Breaks When LLMs Code? Characterizing Operational Safety Failures of Agentic Code Assistants (Hasan & Biswas) — [arxiv.org/abs/2605.30777](https://arxiv.org/abs/2605.30777) | ✅ |
| TDFlow: Agentic Workflows for Test Driven Development — [arxiv.org/pdf/2510.23761](https://arxiv.org/pdf/2510.23761) | ✅ (ek okuma) |
| Spec Kit Agents — çok-ajanlı SDD pipeline'ında context-grounding hook'ları (arXiv 2604.05278) | ⚠ doğrulanmadı |
| Constitutional SDD — CWE eşlemeli güvenlik kısıtlarının spec'e gömülmesi | ⚠ doğrulanmadı |

### Metodoloji

| Kaynak | Durum |
|---|---|
| GitHub Spec Kit — [github.com/github/spec-kit](https://github.com/github/spec-kit) | ✅ |
| Thoughtworks Technology Radar — [thoughtworks.com/radar](https://www.thoughtworks.com/radar) | ✅ |
| TDAD popüler özet — [thelgtm.dev](https://thelgtm.dev/tdad-test-driven-agentic-development-reducing-code-regressions-by-70/) | ✅ |
| Kent C. Dodds — Testing Trophy | ⚠ slug doğrulanmadı |
| O'Reilly Radar — "Why AI Coding Agents Still Need Clear Specs" (U-şeklinde maliyet eğrisi) | ⚠ slug doğrulanmadı |
| Allstacks — spec + TDD katmanlı model, Kent Beck sentezi | ⚠ doğrulanmadı |
| Emily Bache (coding-is-like-cooking) — agentic TDD saha gözlemleri | ⚠ slug doğrulanmadı |
| Microsoft Developer Blog — spec-first AI-native engineering | ⚠ doğrulanmadı |
| Augment Code — SDD kılavuzu, contract/mutation testing rehberleri | ⚠ doğrulanmadı |
| Nick Perkins — agentic geliştirmede test piramidi ve test skill dosyası | ⚠ doğrulanmadı |
| AutomationPanda — `gherkin-guidelines-for-ai` | ⚠ slug doğrulanmadı |
| Meta Engineering — LLM destekli mutation testing (ACH) | ⚠ doğrulanmadı |

**Kural:** `⚠` işaretli bir kaynağı bu repoda yeni bir zorunlu kuralın *tek* gerekçesi olarak kullanmak yasak. Ya doğrula ve `✅` yap, ya kuralı "gerekçeli varsayım" olarak etiketle.
