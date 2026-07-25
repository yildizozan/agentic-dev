# 08 — Pilot Planı

> **Normatif olmayan** — uygulama sırası önerisi. Sıra gerekçesi [`02` §5](02-spec-fidelity.md).

---

## 1. Hafta 1 — zemin

| Gün | İş | Rol | Referans |
|---|---|---|---|
| 1 | Kanıt kaydı: resmi/primary web + Reddit saha taraması, sınırlılık ve karar notu | Tech Lead + **insan** | [`09`](09-web-reddit-field-guide.md) |
| 1 | Hedef reponun CI/ruleset envanteri; prose'da söylenen ile gerçekten çalışan gate ayrılır | Tech Lead + **insan** | [`ci/pipeline.example.yml`](../ci/pipeline.example.yml) |
| 1 | Statik kapılar + derleme + strict tip | Tech Lead ajanı | [`02` §3.3](02-spec-fidelity.md) |
| 1 | **Architecture fitness functions** (katman kuralları) | Tech Lead ajanı | [`04` §2](04-codebase-integrity.md) |
| 1 | `TESTING.md` test taksonomisi skill dosyası | Tech Lead ajanı | [`templates/TESTING.md`](../templates/TESTING.md) |
| 2 | `ownership-map.yml` + `CODEOWNERS` + CI sahiplik gate'i; pre-commit yalnız hızlı geri bildirim | Tech Lead + **insan** | [`03` §1](03-concurrency.md) |
| 2 | **Merge queue** aç, `main`'e doğrudan push'u kapat | **insan** | [`03` §5](03-concurrency.md) |
| 2 | Worktree izolasyonu + branch isimlendirme + ömür sınırı | Tech Lead | [`03` §2](03-concurrency.md) |
| 3 | **Ajan yetki sınırları / sandbox** — yasakları çalıştırılamaz hale getir | **insan** | [`06` §5](06-operations.md) |
| 3 | Secret scan + SCA + Semgrep baseline | Security ajanı | [`02` §3.7](02-spec-fidelity.md) |
| 3 | `.gitattributes` + yüksek çekişmeli dosya politikası; semantik dosyalarda otomatik union/ours yok | Tech Lead | [`03` §6](03-concurrency.md) |
| 4 | AC şablonu + kriter kapsaması kontrolü fast lane'e bağlanır | PM ajanı + Tech Lead | [`02` §2.1](02-spec-fidelity.md) |
| 4 | **Impact analysis skill dosyası** — hangi testi koş | Tech Lead ajanı | [`04` §5](04-codebase-integrity.md) |
| 4 | Grounding protokolü ajan prompt'una gömülür | Tech Lead | [`04` §7](04-codebase-integrity.md) |
| 5 | **Tek feature'ı uçtan uca yeni akışla koştur** | Tüm roller + **insan G1** | §2 |
| 5 | Retro | **insan** + PM + Tech Lead | §3 |

**Not:** Gün 2 ve 3'teki insan işleri (merge queue, sandbox, ownership) ajana devredilemez — ajanın kendi kısıtlarını kurması yapısal olarak yanlıştır ([`05` §5](05-roles.md)).

---

## 2. Gün 5 uçtan uca koşum — adım adım

```
1. PM ajanı: AC-001 yazar + Gherkin taslağı
2. ╔ İNSAN G1: AC'yi protected review/attestation ile onaylar ╗
3. QA ajanı: yeni acceptance oracle'ını path-pure commit A'da yazar
4. Engineer ajanı, yazmadan önce:
   - grounding sorgusu çalıştırır
   - impact analiziyle etkilenen testleri çıkarır
   - AC kapsamı ve sahiplik sınırını doğrular
5. Engineer ajanı çakışmasız claim/lease açar, worktree'de implement eder (commit B)
6. Fast lane; süre pilotta ölçülür, stack SLO'su sonra belirlenir
7. Merge lane adapter'ı commit A'nın beklenen test kimliğinde ve beklenen
   assertion sınıfıyla kırmızı olduğunu doğrular; genel `exit != 0` yeterli değildir
8. Risk sınıflandırma: 🔴 var mı → varsa G2
9. Merge queue: sentetik birleşik SHA üzerinde PR ile aynı required kontroller + E2E
10. Harici, izole gizli evaluator kurulmuşsa black-box sonucu ayrıca alınır
11. main
```

Yeni acceptance oracle'ı aynı entegrasyon PR'ında ayrı, QA-imzalı commit olabilir.
Mevcut kilitli oracle değişikliği ayrı PR ve ayrı tahkim akışıdır. Engineer
unit/integration testleri implementasyonla aynı PR'da tutabilir.

**Bu koşumda ölçülecek 6 şey:**

| Ölçüm | Neyi test ediyor |
|---|---|
| Kaç AC testsiz kaldı | criteria coverage çalışıyor mu |
| Ajan kaç kez kilitli teste dokunmaya çalıştı | [`02` §4.2](02-spec-fidelity.md) etkili mi |
| Kırmızı kanıtı adımı kaç kez "test baştan yeşil" dedi | [`06` §2](06-operations.md) değer üretiyor mu |
| Fast lane p95 süresi | Stack'e özgü SLO ne olmalı |
| İnsan G1 + G2'de kaç dakika harcadı | ölçek sürdürülebilir mi |
| Grounding sorgusu var olan kodu buldu mu | [`04` §7](04-codebase-integrity.md) işe yarıyor mu |

---

## 3. Pilot başarı kriteri

> **Ajan, hiçbir mevcut kilitli oracle'ı değiştirmeden, tüm aktif AC'ler
> doğrulanmış test referansına sahipken, tanımlı insan kapılarından geçerek tek
> feature'ı merge edebiliyor mu?**

Ek olarak **2 ajanla eşzamanlı** ikinci bir koşum (çakışma ekseninin testi):

> **İki ajan aynı modülde eşzamanlı çalışırken lease çakışmasını yazmadan önce
> durdurabiliyor mu; ayrık işlerde sentetik birleşik SHA her iki değişikliğin
> semantik uyumunu doğruluyor mu?**

İkinci koşum atlanmamalı — v1.0'ın kör noktası tam olarak burasıydı.

---

## 4. Hafta 2–4

| Hafta | İş |
|---|---|
| 2 | Contract testleri (bir servis sınırı) + `oasdiff` gözlemi · Regresyon smoke çekirdeği · Flaky politikası ve karantina otomasyonu |
| 3 | Incremental mutation + diff coverage baseline'ı · Duplikasyon + API surface ölçümü · Property-based (para/skor/state machine) |
| 4 | E2E kritik yolculuklar (risk-seçilmiş küçük set) · Deterministik replay (simülasyon içeren modüller) · Spec değişim protokolü canlı deneme |

---

## 5. Baseline ölçüm dönemi (kritik)

**İlk 2 sprint hedef koymadan ölçüm yap.** [`07` §5](07-metrics.md)'teki gerekçe: paper'ların benchmark sayılarını hedef olarak ithal etmek, bu repo'nun eleştirdiği hatanın aynısı. Kendi modellerinle, kendi codebase'inde baseline'ını çıkar, hedefi ondan türet.

Baseline'ı çıkarılacak asgari set: regresyon oranı · merge sonrası kırılma oranı · fast lane süresi · flake oranı · çöpe giden iş oranı · insan review dakikası / AC.

---

## 6. Bilinçli olarak v2'ye bırakılanlar

| Konu | Neden şimdi değil |
|---|---|
| Chaos / fault injection | Efor/getiri oranı olgunlaşmadan kötü |
| Visual regression (screenshot) | UI stabilize olmadan gürültü |
| Prompt/skill dosyaları için eval suite | Önce temel gate'ler ([`05` §5](05-roles.md)) |
| LLM-as-judge otomasyonu | İnsan G5 daha güvenilir |
| Semantic (embedding) duplikasyon taraması | Token/AST katmanı önce |
| Harici gizli evaluator | Ayrı trust boundary, kısıtlı kimlik bilgisi ve kapalı ham log kurulmadan “gizli” iddiası güvenilir değildir; kurulana kadar yalnız pilot önerisidir |
