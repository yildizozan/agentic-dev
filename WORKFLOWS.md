# Hermes Workflow ve Kanban Çalışma Modeli

Bu doküman, Hermes profilleriyle yürütülen yazılım işlerini **koşullu,
artifact-gated bir Kanban DAG** olarak tanımlar. Belirli bir ürün, framework veya
repository için yazılmamıştır.

> Bu dosya tek başına çalışan native bir Hermes workflow DSL'i değildir.
> Workflow şablonunu Kanban kartlarına dönüştüren bir orchestrator/controller
> gerekir. Dosya ayrıca profil, board, gateway, push, merge, release veya deploy
> oluşturma yetkisi vermez.

Hermes profilleri birbirinden bağımsız config, kimlik, memory, session ve skill
alanlarına sahiptir
([resmî profil dokümanı](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)).
Hermes Kanban ise profiller arasında kalıcı görev, durum ve handoff kaydı tutar
([resmî Kanban dokümanı](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban)).

## 1. Hedef model

```text
Onaylı talep
    ↓
Workflow seçimi ve immutable workflow instance
    ↓
Koşullu Kanban DAG
    ↓
Tek sahipli profil kartları
    ↓
Şemalı artifact + gerçek doğrulama
    ↓
Riskin gerektirdiği bağımsız gate'ler
    ↓
Yetkilendirilmiş teslimat
```

LLM çözüm üretir; workflow kapsamı ve kanıtı sınırlar. Deterministik olması
beklenen LLM cevabı değil, controller'ın graph üretimi, lifecycle geçişleri,
idempotency ve side-effect denetimidir.

## 2. Beş ayrı sorumluluk

| Katman | Sorduğu soru | Sahip olduğu şey |
|---|---|---|
| **Profile** | Bu işi kim yapar? | Kalıcı kimlik, rol sınırı, model, tools, skills, memory |
| **Workflow** | Bu iş nasıl tamamlanır? | Aşamalar, koşullar, inputs, outputs, gate ve failure politikası |
| **Orchestrator** | Hangi kartlar oluşturulmalı? | Workflow seçimi, kart kapsamı, owner ve dependency graph |
| **Kanban + dispatcher** | İş ne durumda ve kim çalıştıracak? | Durable state, atomik claim, worker başlatma, retry/reclaim |
| **Artifacts** | Ne üretildi ve nasıl doğrulandı? | Şemalı çıktı, exact source ref, evidence, verdict, residual risk |

Bu sınırlar birbirinin yerine geçmez. Profil mesajı kart oluşturmaz; kart
oluşturmak da worker'ın başladığını kanıtlamaz; heartbeat ise artifact veya
canlı worker kanıtı olmadan ilerleme sayılmaz.

## 3. Tek dispatcher ve lifecycle ilkesi

- Yalnız canonical gateway Kanban kartlarını dispatch eder.
- Orchestrator kartları oluşturur, kapsamlar, atar ve bağlar; process spawn etmez.
- Profil gateway'leri iletişim yüzeyidir; ikinci dispatcher değildir.
- Canonical gateway dispatch ederken ayrıca `hermes kanban daemon` çalıştırılmaz.
- Workflow adapter'ı varsa tek mutation arbiter üzerinden Kanban'a yazar; ayrı bir
  queue veya ikinci lifecycle state machine kurmaz.
- Otomatik decomposition varsayılan çözüm değildir. Orchestrator yalnız gerekli
  minimum graph'ı açıkça oluşturur.

Native task lifecycle:

```text
triage | todo | ready | running | blocked | done | archived
```

- `ready`, bütün prerequisite'leri tamamlanmış ve dispatch edilebilir karttır.
- `blocked`, gerçek input/capability/access/transient engel içindir.
- Yalnız parent beklemek sticky blocker değildir; dependency graph ile temsil edilir.
- `done`, kartın işi tamamlandı demektir; gate verdict'ünün `PASS` olduğu anlamına
  gelmez.

Kanban bağlantısı prerequisite yönündedir:

```text
A → B  =  A tamamlanmadan B çalışamaz
```

Organizasyon şeması ile dependency graph aynı şey değildir.

## 4. Profile ne konur?

Profil, tek bir görev veya workflow aşaması değil, tekrar eden kalıcı bir
rol/capability sınırıdır. Sadece isim simetrisi için profil açılmaz.

| Bilgi | Doğru yer |
|---|---|
| Ses, ton, itiraz ve rol sınırı | Profil `SOUL.md` |
| Model, tools, skills ve capability | Profil config'i |
| Routing için kısa rol tarifi | Profil description |
| Framework, path, port ve gerçek komutlar | Proje `AGENTS.md` / `.hermes.md` |
| Göreve özel input, scope ve doğrulama | Kanban kartı |
| Aşamaların sırası ve koşulları | Workflow şablonu |
| QA/Security/Review sonucu | Şemalı artifact ve Kanban metadata |

Bir profil local terminalde filesystem sandbox değildir. Yazma sınırı task'ın
exact workspace'i, tool yetkisi, repository korumaları ve gerektiğinde OS/container
izolasyonuyla uygulanır.

## 5. Rol sınırları

### İnsan karar sahibi

- Ürün/risk kabulü, dış hesap mutation'ı, merge ve production deploy gibi ayrılmış
  yetkilerin son sahibidir.
- Açık bir Issue'yu tek başına execution izni saymaz.

### Project Manager / Workflow Orchestrator

- Talebi normalize eder; priority, acceptance criteria ve kapsam dışını yazar.
- Uygun workflow'u seçer ve Kanban DAG'ını oluşturur.
- Her karta bir owner, artifact contract ve terminal koşul atar.
- Kod yazmaz, mimari seçmez, QA/Security verdict'ü üretmez ve teknik çözümü dikte
  etmez.
- İnsan product owner'ın veya risk sahibinin yerine kendiliğinden geçmez.

### Product Designer — koşullu

UI, UX, user flow, accessibility veya design contract değişiyorsa çalışır.
Ürettiği `product_spec`, user journey, durumlar, ölçülebilir UX kriterleri,
design tokens ve açık kararları içerir. Ürün kapsamını veya implementasyon
tekniğini belirlemez.

### Tech Lead — koşullu

Mimari sınır, ortak contract, migration, çok bileşenli veya yüksek riskli değişimde
çalışır. Implementation-ready `technical_plan` ve gerektiğinde ADR üretir.
Kabul kriterini yazmaz ve implementerin kodunu üstlenmez. Riskli ya da çok dosyalı
değişiklikte bağımsız teknik review yapabilir.

### Software Engineer

Acceptance criteria, gerekli product/technical artifact'lar, exact workspace,
yazma kapsamı ve verification contract'tan çalışır. Kod, uygun testler ve gerçek
analyze/lint/typecheck/build/test kanıtı üretir. Test sırası metodoloji olarak
zorunlu değildir; davranış değişikliği için uygun regression kanıtı zorunludur.

### QA Engineer

Kabul kriteri ile exact artifact/commit arasındaki uyumu bağımsız sınar. Üretim
kodu yazmaz ve kriter icat etmez. Çıktısı `PASS`, `FAIL` veya `INCONCLUSIVE`
verdict'lü bir `qa_verdict` artifact'ıdır; QA kaliteyi garanti ettiğini iddia etmez.

### Security Engineer — profil kalıcı, gate koşullu

Trust boundary, auth/authz, secret, privileged field, API exposure, dependency,
data ownership veya abuse path değişiyorsa çalışır. Sömürülebilirlik, önkoşul,
etki, kanıt ve residual risk içeren `security_verdict` üretir. Riski kabul etmez;
karar sahibine görünür kılar.

### Challenge / Devil's Advocate — koşullu

Yeni mimari, maliyet/ölçek kararı, kritik user flow, migration, güvenlik sınırı
veya çok repository'li değişiklikte bir kez çalışır. Amacı sınırsız eleştiri
değil, varsayımları sınamaktır. `challenge_review` şu alanları içerir:

- challenged assumptions
- evidence ve counterexamples
- severity ve impact
- required changes
- verdict: `PASS | REQUEST_CHANGES | INCONCLUSIVE`

Küçük, tek dosyalı ve düşük riskli değişiklik için zorunlu gate değildir.

### Release Engineer — koşullu

Tekrarlanan release işi ayrı capability, tool ve yetki gerektiriyorsa kalıcı
profil olur. Exact merge commit, build matrix, artifact, signing/provisioning,
migration sırası, release note, rollback ve smoke check üretir. Build yetkisi
merge veya deploy yetkisi değildir.

Varsayılan bir `Director` profili gerekmez. Kalıcı portföy karar yetkisi gerçekten
bir ajana devredilmişse ayrıca tanımlanabilir; routine dispatcher olamaz.

## 6. Universal Kanban kart sözleşmesi

Her runnable kart tek owner taşır ve kendi başına anlaşılır olmalıdır. Native
Kanban alanları (`assignee`, `parents`, `workspace`, `tenant`, `skills`,
`idempotency_key`) prose içine gömülmek yerine native alanlara yazılır.
Aşağıdaki kalan sözleşme kart body/metadata'sında tutulabilir:

```yaml
task:
  mode: code_change # operations | research | monitoring | content_design
  objective: "Gözlemlenebilir tek sonuç"
  owner: "<profile>"

  inputs:
    - type: requirement
      ref: "<immutable-source-ref>"

  needs: []

  expected_artifact:
    type: implementation_bundle
    schema_version: 1

  workspace:
    kind: worktree # dir | scratch
    path: "<absolute-path>"
  tenant: null

  scope:
    allowed: ["<bounded-path-or-system>"]
    forbidden: ["<explicit-boundary>"]

  allowed_side_effects:
    local_write: true
    commit: true
    push: false
    open_pr: false
    merge: false
    deploy: false

  verification:
    - "<real command or inspection>"

  terminal_condition:
    complete: "Artifact ve bütün zorunlu evidence üretildi"
    block: "Gerekli input, capability veya yetki yok"

  failure_policy:
    retry_limit: 1
    rollback: "<rollback unit or not_applicable>"

  turn_budget: 80
  timeout_minutes: 30
  idempotency_key: "<workflow-instance>:<stage>:<source-revision>"
```

Kart modu evidence türünü değiştirir:

| Mode | Tamamlanma kanıtı |
|---|---|
| Code change | Diff/commit, ilgili test/analyze/build sonucu, izin verilmişse PR state |
| Operations | Target, önce/sonra status, exact command result, rollback/unrun check |
| Research | Kaynak, snapshot zamanı, yöntem, varsayım ve rapor/dataset |
| Monitoring | Aralık, signal, threshold, sonuç veya açık `no finding` |
| Content/design | İstenen artifact, constraint ve review kriterleri |

## 7. Workflow, liste değil koşullu DAG'dır

```text
intake
  ├── product_spec? ──────┐
  └── technical_plan? ────┼── challenge? ──┐
                          └─────────────────┼── implementation(s)
                                             │      (paralel olabilir)
                                             ↓
                                   QA? / Security? / Technical review?
                                             ↓
                                      readiness audit
                                             ↓
                                    delivery / PR-ready
                                             ↓
                                  release? (ayrı yetki)
```

`?` koşullu stage demektir. Koşul false ise native Kanban'a sahte bir status
eklenmez; workflow instance metadata'sında `skipped` disposition ve gerekçesi
kaydedilir. Adapter, skipped stage dependency'sini kart oluşturmadan çözer.

Minimum gate seçimi:

| Değişiklik | Gerekli graph |
|---|---|
| Trivial, davranış değiştirmiyor | Implementasyon → readiness audit |
| Davranış değişikliği | Implementasyon → bağımsız QA → readiness audit |
| UI/UX kararı | Product spec → implementasyon → design/QA gate gerektiği kadar |
| Trust boundary | Technical plan → implementasyon → Security → readiness audit |
| Mimari/migration/yüksek risk | Plan → Challenge → implementasyon → bağımsız gate → final review |
| Release | Readiness PASS → exact-commit release kartı → yetkili deploy gate'i |

## 8. Workflow şablonu sözleşmesi

Workflow şablonu project-local bir convention olabilir; Hermes'in kendiliğinden
okuduğu native dosya olduğu varsayılmaz. Adapter, şablonu immutable bir workflow
instance'a ve minimum Kanban graph'ına dönüştürür.

```yaml
schema: hermes.workflow/1
id: feature-development
revision: 1

entry:
  required_approval: true
  source_types: [issue, requirement]

stages:
  - id: intake
    owner: project-manager
    needs: []
    produces: requirement_spec
    when: always

  - id: product_spec
    owner: product-designer
    needs: [intake]
    produces: product_spec
    when: affects_ui_or_user_flow

  - id: technical_plan
    owner: tech-lead
    needs: [intake, product_spec]
    produces: technical_plan
    when: crosses_contract_or_risk_is_normal_or_higher

  - id: challenge
    owner: challenge-reviewer
    needs: [product_spec, technical_plan]
    produces: challenge_review
    when: risk_is_high

  - id: implementation
    owner: "<implementation-profile>"
    needs: [intake, product_spec, technical_plan, challenge]
    produces: implementation_bundle
    when: always

  - id: qa
    owner: qa
    needs: [implementation]
    produces: qa_verdict
    when: changes_observable_behavior

  - id: security
    owner: security
    needs: [implementation]
    produces: security_verdict
    when: changes_trust_boundary

  - id: technical_review
    owner: tech-lead
    needs: [implementation]
    produces: technical_review
    when: risk_is_normal_or_higher

  - id: readiness
    owner: project-manager
    needs: [implementation, qa, security, technical_review]
    produces: readiness_audit
    when: always

  - id: release
    owner: release-engineer
    needs: [readiness]
    produces: release_manifest
    when: release_requested_and_authorized
```

Her stage ayrıca Universal Kanban kart sözleşmesindeki `inputs`, `workspace`,
`tenant`, `allowed_side_effects`, `verification`, `terminal_condition`,
`turn_budget`, `timeout` ve `idempotency_key` alanlarını çözmelidir. Çözülmemiş
owner/workspace/approval bulunan stage fail-closed kalır; dispatch edilmez.

Birden fazla implementer gerektiğinde tek `implementation` kartı paylaşılmaz.
Ortak contract artifact'ından sonra ayrı owner'lı kartlar paralel oluşturulur ve
sonraki gate'ler hepsine prerequisite olarak bağlanır.

## 9. Artifact sözleşmesi

Dosya adı artifact sözleşmesi değildir. Her artifact şemalı ve kaynağa bağlıdır:

```yaml
artifact:
  type: qa_verdict
  schema_version: 1
  workflow_instance: "<stable-id>"
  stage: qa
  producer: qa
  source_ref: "<issue-or-requirement-revision>"
  repository: "<repository-id-or-null>"
  exact_commit: "<sha-or-null>"
  parent_artifacts: ["<artifact-ref>"]
  evidence:
    commands: []
    attachments: []
  verdict: PASS # FAIL | REQUEST_CHANGES | INCONCLUSIVE | null
  residual_risks: []
  lifecycle_disposition: completed
```

- ADR, kalıcı architecture contract, design token, public data contract ve migration
  belgesi repository'de yaşar.
- Test/build log'u, screenshot, QA/Security verdict'ü ve release candidate manifest'i
  Kanban attachment veya structured completion metadata olabilir.
- Controller authority'si serbest metin comment değil, native graph ve structured
  metadata'dır. Comment açıklama ve audit trail içindir.

## 10. Lifecycle, verdict ve rework

- Worker acceptance ve evidence tamamlanınca `kanban_complete` çağırır.
- Eksik karar, erişim, capability veya bounded dış hata varsa `kanban_block` çağırır.
- Sadece parent beklemek gerçek bir sticky blocker değildir; dependency graph ile
  temsil edilir.
- `done`, kartın işinin bittiğini söyler; gate'in `PASS` verdiğini söylemez.
- QA/Security/Review kartı raporunu tamamlayıp `FAIL` verdict'üyle `done` olabilir.
- Her `FAIL`, source commit + normalize bulgular üzerinden **bir** idempotent rework
  kartı üretir.
- Rework `C2` commit'i üretirse `C1` review kartları yeniden kullanılmaz. `C2` için
  fresh QA/Security/Review kartları oluşturulur.
- Eski generation audit için korunur; yeni işi başlatmak için silinmez veya yeniden
  açılmaz.
- Terminal state uyuşmazlığında mevcut verified artifact uzlaştırılır; duplicate
  implementation kartı açılmaz.

## 11. Issue intake ve authorization

Issue bir gereksinim kaynağıdır; tek başına execution veya external mutation izni
değildir.

Workflow instance şu bilgileri sabitler:

- source repository ve Issue/requirement kimliği
- onay sinyali ve onaylayan authority
- kabul edilen revision/hash
- acceptance criteria ve kapsam dışı
- seçilen workflow id/revision
- board, tenant ve workspace

Kaynak içerik dispatch sonrası değişirse aktif worker'ın kapsamı sessizce büyümez.
Reconciliation ve gerekiyorsa yeniden onay gerekir. GitHub veya başka backlog
sistemi ürün gerçeği, Hermes Kanban execution gerçeği olabilir; iki state machine
körlemesine birbirine aynalanmaz.

## 12. Side-effect ve release gate'leri

Şu yetkiler birbirinden bağımsızdır:

```text
local write ≠ commit ≠ push ≠ PR açma ≠ merge ≠ build ≠ deploy
```

Her external veya geri döndürülmesi pahalı işlem kartta açıkça yetkilendirilir.
Yetki yoksa worker hazırlık artifact'ını tamamlar ve işlemi yapmaz.

Release artifact'ı en az şunları içerir:

- exact merged commit
- target/environment
- build matrix ve gerçek sonuçlar
- produced artifact kimliği/hash'i
- signing/provisioning durumu
- migration sırası
- deploy authorization
- rollback planı
- post-deploy smoke check
- çalıştırılmayan kontroller

## 13. Deterministik controller ilkeleri

Controller şu invariants'ları sağlamalıdır:

1. Aynı workflow instance/stage/source revision için duplicate kart üretmez.
2. Her kartın tek owner'ı ve exact workspace'i vardır.
3. Dependency yönü `prerequisite → dependent` olarak read-back ile doğrulanır.
4. Review artifact'ı exact commit'e bağlıdır; stale artifact reddedilir.
5. Koşullu stage'ler için `executed` veya gerekçeli `skipped` disposition kaydedilir.
6. Human approval gerektiren side effect fail-closed kalır.
7. Retry, rework, needs-input ve capability failure birbirinden ayrılır.
8. Mutasyon tek arbiter üzerinden yapılır; ikinci dispatcher kurulmaz.
9. Card create/link sonrası native board state tekrar okunur.
10. Heartbeat tek başına başarı veya ilerleme kanıtı sayılmaz.

External workflow engine ancak Kanban'ın ifade edemediği ölçülmüş bir ihtiyaç varsa
değerlendirilir. İlk çözüm native Kanban DAG ve küçük bir adapter'dır; ikinci bir
queue veya dispatcher değildir.

## 14. Dosyaların yeri

| Artifact | Yer |
|---|---|
| Profil identity | `~/.hermes/profiles/<name>/SOUL.md` |
| Profil config/skills/tools | `~/.hermes/profiles/<name>/` |
| Proje kuralları | Repository `AGENTS.md` veya `.hermes.md` |
| Workflow şablonları | Örneğin `.hermes/workflows/` — yalnız project convention |
| Kalıcı mimari/ürün sözleşmesi | Repository'de ilgili sahipli path |
| Geçici gate evidence | Kanban metadata/attachment |

`WORKFLOWS.md` runtime tarafından otomatik yüklenmez. `.hermes/workflows/` da bir
adapter/controller olmadan execution üretmez. Bir dosyanın varlığı lifecycle
entegrasyonu kanıtı değildir.

## 15. Başarı ölçütleri

- Approved request → PR-ready lead time
- İnsan müdahalesi sayısı
- Duplicate card/graph oranı
- Stale `blocked` veya review generation sayısı
- First-pass gate `PASS` oranı
- Rework döngüsü sayısı
- Artifact schema completeness
- Exact-commit gate coverage
- Yetkisiz side-effect sayısı — hedef `0`
- Release rollback readiness
- Aynı workflow'un tekrarlı ve kararlı tamamlanma oranı

## 16. Tamamlanma kontrolü

Bir workflow “çalışıyor” sayılmadan önce:

- [ ] Workflow revision immutable instance'a sabitlendi.
- [ ] Her runnable kartın tek owner, native dependency ve exact workspace'i var.
- [ ] Koşullar minimum graph üretiyor; zorunlu waterfall yok.
- [ ] Her stage şemalı artifact ve terminal koşul taşıyor.
- [ ] QA/Security/Review status ile verdict'ü ayırıyor.
- [ ] Rework yeni commit için fresh gate generation oluşturuyor.
- [ ] Push/merge/deploy ayrı ve açık yetki gerektiriyor.
- [ ] Canonical gateway dışında dispatcher çalışmıyor.
- [ ] Gerçek board read-back ve en az bir bounded canary tamamlandı.
