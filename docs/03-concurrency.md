# 03 — Multi-Agent Eşzamanlılık Protokolü

> **Normatif.** Bu dosya v1.0'da yoktu — repo'nun ilan ettiği ikinci amaç (*"ajanlar birbirinin ayağına basmasın, birbirinin değişikliğini bozmasın"*) yazılmamıştı.
> Kapsam: aynı anda çalışan N ajanın birbirini bozmasını **önlemek**.

---

## 0. Neden contract testleri yetmez

Bu dosyanın var olma sebebi tek bir ayrım:

> **Contract testleri desync'i *yakalar*. Çakışmayı *önlemez*.**

Bunlar iki farklı problem sınıfı:

| | Desync | Çakışma |
|---|---|---|
| Ne | Backend ajanı şemayı değiştirdi, Flutter ajanı eski şemaya göre yazdı | İki ajan aynı dosyayı aynı anda yazdı |
| Ne zaman görünür | Contract test kırıldığında (post-hoc) | Merge sırasında, ya da hiç görünmez (semantik çakışma) |
| Çözüm | Contract test → [`02` §3.2](02-spec-fidelity.md) | **Bu dosya** |

Ve kritik olan üçüncü durum:

> **İki PR'ın da izole halde yeşil olması, merge sonrası yeşil olacağı anlamına gelmez.**
> Ajan A `calculateTotal()` davranışını değiştirir; Ajan B eski davranışa bağımlı yeni kod yazar. İkisi de kendi branch'inde yeşildir. Merge sonrası main kırmızıdır. Bunu **yalnız merge queue** yakalar (§5).

---

## 1. Katman 1 — Governance ownership (ZORUNLU)

İki kavram ayrıdır:

- **Governance owner:** path için kim review/onay verir (`CODEOWNERS`).
- **Aktif write lease:** o anda path'e kim yazabilir (§4).

Statik owner bir eşzamanlılık kilidi değildir. Aynı domain'e farklı zamanlarda
birden fazla ajan katkı verebilir; aynı anda çakışmayı lease önler.

Sahiplik haritası repoda makine-okunur olarak tutulur: [`templates/ownership-map.yml`](../templates/ownership-map.yml)

> **Geçiş notu:** Bu korumalı şablonun mevcut sürümü legacy “statik owner =
> aktif yazar” ve lockfile kurallarını taşımaya devam ediyor. Tech Lead + insan
> sahibi §1 ve §6 ile uzlaştırmadan hedef repoya kopyalanmamalıdır.

```yaml
# ownership-map.yml (örnek)
domains:
  - path: "src/billing/**"
    owner: agent:backend
    contention: high        # para → insan review zorunlu
  - path: "src/ui/**"
    owner: agent:frontend
  - path: "contracts/**"
    owner: agent:techlead    # feature ajanları yazamaz
  - path: "tests/acceptance/**"
    owner: agent:qa
  - path: "db/migrations/**"
    owner: agent:migration   # tek sahip, bkz. §6
```

**Uygulama:** `CODEOWNERS` review sorumluluğunu, CI rol/path yetkisini, claim
servisi aktif yazarı uygular. Pre-commit yalnız hızlı geri bildirimdir ve güvenlik
sınırı değildir.

**Sahiplik dışına yazma gerekirse:** ajan yazamaz, **istek açar**. Sahibi olan ajan ya kendisi yapar ya sahipliği geçici devreder. Bu bir insan onay noktası değil, ajanlar arası protokol adımıdır.

---

## 2. Katman 2 — Fiziksel izolasyon (ZORUNLU)

| Mekanizma | Kural |
|---|---|
| **Worktree per agent** | Her ajan kendi git worktree'sinde çalışır. Ortak çalışma dizini paylaşan iki ajan birbirinin yarım işini görür ve üstüne yazar. Claude Code'da `EnterWorktree`; genel olarak `git worktree add`. |
| **Branch per task** | `agent/<rol>/<AC-###>-<kısa-slug>`. Bir branch = bir görev = bir PR. |
| **Branch ömür bütçesi** | İlk baseline'da ölçülür; hedef repo kendi süre/diff bütçesini tanımlar. Uzayan branch otomatik uyarı ve yeniden-scope üretir. |
| **Rebase, merge değil** | Feature branch'ler `main`'e rebase edilir. Merge commit'li ajan branch'lerinde çakışma arkeolojisi imkânsız hale gelir. |
| **Force-push yasağı** | Paylaşılan branch'lere force-push YASAK → [`06` §5](06-operations.md). |

---

## 3. Katman 3 — Interface freeze sıralaması (ZORUNLU)

**Kural: Contract merge edilmeden paralel implementasyon başlamaz.**

v1.0 bunu ima ediyordu ama sıralama kuralı haline getirmemişti. Doğru akış:

```
1. Tech Lead ajanı contract'ı yazar        (contracts/**)
2. Contract kendi PR'ında merge edilir     ← BARİYER
3. Stub/client, repo'nun tek generated-code politikasına göre üretilir (§6)
4. ANCAK ŞİMDİ feature ajanları paralel açılır
```

**Anti-pattern:** Backend ve Flutter ajanını aynı anda "şemayı da sen tasarla" diyerek açmak. İki ajan iki farklı şema tasarlar; contract testi bunu ancak ikisi de bittikten sonra yakalar ve o noktada işin yarısı çöpe gider.

**Contract donduktan sonra değişirse:** breaking change → `oasdiff` gate → insan onayı + spec-change protokolü → [`06` §4](06-operations.md). Devam eden feature ajanlarına **bildirim gitmesi zorunludur** (§4.3).

---

## 4. Katman 4 — Claim / lease protokolü

Ajan önce AC'yi ve codebase'i **read-only** inceler; dokunacağı sembol/path'ler
belirlendikten sonra, ilk yazmadan hemen önce claim açar. Path'i keşfetmeden claim
açmak ya aşırı geniş kilit ya da eksik rezervasyon üretir.

### 4.1 Claim kaydı

Gerçek paralel/dağıtık kullanımda tek doğruluk kaynağı atomik compare-and-set
destekleyen issue tracker/GitHub App/lock servisidir. Repodaki `tasks/active/`
yalnız tek-orchestrator pilotunda **manual** kontroldür; iki host için kilit değildir.
Minimum alanlar:

```yaml
task: AC-042
agent: agent:backend#7
branch: agent/backend/AC-042-invoice-rounding
claimed_paths:
  - src/billing/invoice.rb
  - src/billing/rounding.rb
lease_expires: 2026-07-25T18:00:00Z    # TTL zorunlu
heartbeat_at: 2026-07-25T14:00:00Z
fencing_token: 17                       # her yeniden-acquire'da monoton artar
depends_on:
  - contract:payments-v3
status: in_progress
```

### 4.2 Lease kuralları

- **TTL zorunlu.** Süresiz claim yoktur. Süre risk, branch ömrü ve heartbeat
  sıklığına göre repo policy'sinde belirlenir.
- **TTL dolması tek başına güvenli release değildir.** Lock servisi fencing token'ı
  artırır; eski token'lı ajan sonraki write/push'ta reddedilir. Heartbeat ve fencing
  yoksa otomatik release yapılmaz, insana escalate edilir.
- **Claim çakışması → ikinci ajan başlamaz.** Bekler veya görevi başka bir path'e böler. "Ben de yazayım, sonra merge ederiz" YASAK.
- **Claim'siz yazılan PR**, ancak hedef repo claim kuralını gerçekten CI/lock
  servisiyle uyguluyorsa otomatik reddedilir. Bu rehber yalnız prosedürü tarif eder.

### 4.3 Invalidation bildirimi (ZORUNLU)

Bir claim'in dayandığı varsayım bozulduğunda **açık claim sahiplerine bildirim gitmek zorundadır.** Tetikleyiciler:

| Olay | Kime bildirilir |
|---|---|
| Contract değişti | O contract'a bağlı tüm açık claim'ler |
| Dayandığı AC v2'ye geçti | O AC'yi claim eden ajan → [`06` §4](06-operations.md) |
| Claim ettiği path'te başka bir PR merge oldu | Rebase + fast lane yeniden koşum zorunlu |

Bildirim yoksa ajan eski gerçekliğe göre çalışmaya devam eder — bu, multi-agent'ta en pahalı sessiz hata sınıfıdır.

---

## 5. Katman 5 — Merge queue (ZORUNLU)

Merge queue, izole PR sonucuyla birleşik state arasındaki farkı görünür kılan
temel katmandır. Kurulum eforu provider, required-check sayısı ve batch
stratejisine göre ölçülür.

```
PR yeşil (izole)  →  merge queue  →  main
                         │
                         ├─ queue güncel main ile sentetik merge-group SHA üretir
                         ├─ PR'daki TÜM required check'leri bu SHA'da yeniden koşar
                         ├─ dış/izole hidden evaluator ayrı required check üretir
                         └─ kırmızıysa PR queue'dan düşer, main temiz kalır
```

Kurallar:

1. **`main`'e doğrudan push YASAK.** Tüm merge'ler queue üzerinden.
2. **Serileştirme.** Queue aynı anda tek PR entegre eder (veya batch + bisect ile bölme).
3. **Birleşik-state doğrulaması.** Unit, integration, acceptance, contract, fitness
   ve repo-kalibreli kalite gate'lerinin aynı check adları `merge_group` event'inde
   de çalışır. Yalnız hidden/E2E koşmak merge queue garantisi değildir.
4. **Hidden evaluator ayrıdır.** PR kontrollü runner hidden token/test dosyası görmez
   → [`02` §4.3](02-spec-fidelity.md).

Araç: GitHub merge queue, Mergify, Zuul, ya da `bors`. Hangisi olduğu önemsiz; olmaması kabul edilemez.

---

## 6. Katman 6 — Yüksek çekişmeli dosya politikası (ZORUNLU)

Ajan çakışmalarının çoğu iş mantığı dosyalarında değil, **merkezi paylaşılan dosyalarda** olur. v1.0 bunlardan hiçbirini ele almıyordu. Her satır bir politika:

| Yüzey | Neden çakışır | Politika |
|---|---|---|
| **Lockfile** (`package-lock.json`, `pubspec.lock`, `Podfile.lock`, `Cargo.lock`) | Her ajan yeniden üretir, tüm dosya değişir | Bağımlılık manifesti + lockfile aynı `agent:deps` PR'ında commit edilir. CI temiz checkout'ta yeniden üretip diff olmadığını doğrular. `merge=ours` ile değişiklik düşürülmez. |
| **DB migration** | Sıralı numaralandırma (`003_`, `004_`) = garantili çakışma | **Timestamp/ULID isimlendirme** (`20260725T143000_add_index.sql`). Migration **daima kendi PR'ında**, asla feature koduyla birlikte. Tek `agent:migration` sahibi. Geri alınabilirlik zorunlu. |
| **Generated kod** (`*.g.dart`, OpenAPI client, protobuf, ORM tipleri) | Şemadan üretiliyor, herkes yeniden üretiyor | Dağıtım/reproducibility ihtiyacına göre policy seçilir. Commit edilmiyorsa CI build artefaktı üretir; ediliyorsa kaynakla deterministik diff doğrulanır + tek sahip. `merge=ours` yok. |
| **Registry / barrel / DI / route tablosu** (`index.ts`, `routes.rb`, DI modülü) | Merkezi, append-only, herkes dokunuyor | Öncelik statik keşfedilebilir modüler kayıt. Auto-discovery yalnız görünürlük/güvenlik maliyeti kabul edildiyse. Otomatik `merge=union` yok; parser + duplicate semantic key gate'i kullan. |
| **i18n / resource dosyaları** | Her ajan anahtar ekliyor | Deterministik format + duplicate/öksüz key kontrolü. `merge=union` semantik doğrulama olmadan kullanılmaz. |
| **Unity sahne** (`*.unity`) | YAML ama **semantik olarak birleştirilemez**. En ciddi kalem. | ① Force Text Serialization ② `UnityYAMLMerge` merge tool olarak kurulu ③ **Sahne için özel claim (exclusive lease)** — aynı sahneye iki açık PR YASAK ④ Feature = kendi prefab'ı; sahneye kompozisyonu **tek integrator ajan** yapar. |
| **Unity prefab** (`*.prefab`) | Aynı sebep | Feature başına ayrı prefab. Paylaşılan prefab'a dokunmak sahne kuralıyla aynı → exclusive claim. Prefab variant kullan. |
| **Unity `.meta`** | GUID churn; asset taşıma tüm referansları kırar | `.meta` **daima** asset'iyle aynı commit'te. Feature PR'ında **asset taşıma/rename YASAK** — ayrı PR. `.meta` asla elle üretilmez/silinmez. |
| **Xcode `.pbxproj` / Gradle** | XML/DSL, merge kâbusu | Mümkünse file-system-synced group / SPM. Değilse tek sahip + ayrı PR. |
| **CI workflow dosyaları** | Herkes gate ekliyor | Tek `agent:techlead` sahibi. |

Kopyalanabilir başlangıç: [`templates/gitattributes.example`](../templates/gitattributes.example)

---

## 7. Katman 7 — Semantik çakışma (en zoru)

Textual conflict yoktur, iki PR da yeşildir, yine de sistem bozulur. Üç desen:

### 7.1 Paralel yeniden-icat
İki ajan bağımsız olarak `formatCurrency` / `retryWithBackoff` yazar. Git çakışma görmez. Codebase iki gerçeğe sahip olur.
→ **Tespit:** duplikasyon/benzerlik taraması + yazmadan önce zorunlu index sorgusu → [`04` §3](04-codebase-integrity.md)

### 7.2 Davranış kayması altında bağımlılık
Ajan A bir fonksiyonun sözleşmesini sessizce değiştirir; Ajan B eski sözleşmeye güvenir.
→ **Tespit:** merge queue (§5) + impact analysis ile etkilenen testlerin koşulması → [`04` §5](04-codebase-integrity.md)

### 7.3 Paralel implementasyon yolu
İkinci bir auth yolu, dördüncü bir HTTP client, ikinci bir cache katmanı. Tüm testler geçer.
→ **Tespit:** architecture fitness functions + bağımlılık gate'i → [`04` §2, §4](04-codebase-integrity.md)

**Kritik nokta:** Bu üçünün hiçbirini test suite yakalamaz. Bu yüzden [`04`](04-codebase-integrity.md) ayrı bir eksen olarak var.

---

## 8. Görev bölme kuralları (çakışmayı kaynağında azalt)

En iyi çakışma çözümü, çakışmayacak şekilde bölmektir.

| Kural | Gerekçe |
|---|---|
| **Dikey bölme, yatay değil.** Görev = uçtan uca ince dilim (bir endpoint + onun modeli + onun testi). "Tüm modelleri sen yaz, tüm controller'ları o yazsın" YASAK. | Yatay bölme her görevi her dosyaya dokundurur → maksimum çakışma. |
| **Bir görev = bir domain sahipliği.** Görev iki domain'e dokunuyorsa iki göreve böl, aralarına contract koy. | §1 ile tutarlılık. |
| **Paralellik derecesini çekişmeye göre seç.** Aynı modülde 5 ajan çalıştırmak, 2 ajan çalıştırmaktan *yavaştır* (rebase + yeniden koşum maliyeti). | Ölçüm: §9 aynı-dosya eşzamanlılık oranı. |
| **Doğal modül sınırını koru.** Yalnız çakışmadan kaçmak için yeni dosya üretme; mevcut abstraction doğru yerse onu genişlet. | Aksi halde çakışma azalırken dosya/abstraction parçalanması büyür. |
| **Sıralı zorunluluk varsa paralel açma.** Migration → model → endpoint zinciri paralelleştirilemez. | Sahte paralellik en pahalı hata. |

---

## 9. Çakışma metrikleri (ZORUNLU ölçüm)

v1.0'ın 5 metriğinin hiçbiri çakışmayı ölçmüyordu — repo'nun ilan ettiği amaç buyken. Bunlar [`07`](07-metrics.md)'ye eklendi:

| Metrik | Başlangıç kullanımı | Neyi yakalar |
|---|---|---|
| **Merge sonrası kırılma oranı** | Baseline → düşüş hedefi | Merge queue eksikliği / semantik çakışma |
| **Aynı-dosya eşzamanlılık oranı** (aynı dosyaya dokunan eşzamanlı açık PR) | Gözlem → görev bölme bütçesi | Kötü görev bölme (§8) |
| **Merge conflict oranı** (conflict yaşayan PR / toplam) | Baseline → repo eşiği | Sahiplik ihlali, uzun branch ömrü |
| **Branch ömrü** | p50/p95 ölç → stack SLO'su | §2 ihlali; çakışmanın öncü göstergesi |
| **Rebase sayısı / PR** | Gözlem | Aşırı paralellik |
| **Revert oranı** | Baseline → düşüş hedefi | Yakalanmamış semantik çakışma |
| **Claim ihlali sayısı** | Değişmez: 0 | Protokol uyumu |

---

## 10. Anti-pattern listesi

| ❌ Anti-pattern | Neden kötü |
|---|---|
| Ajanların ortak çalışma dizinini paylaşması | Birbirinin yarım işini okur/üstüne yazar |
| Merge queue olmadan paralel ajan | "İzole yeşil" hiçbir şey garanti etmez |
| Sahipliği yalnız `CODEOWNERS` ile kurmak | Review ister, yazmayı engellemez |
| Contract'ı paralel ajanlara tasarlatmak | İki farklı şema, işin yarısı çöpe |
| Lockfile/migration/generated stratejisini tanımlamadan paralel düzenlemek | Sessiz kayıp, drift veya sık çakışma |
| Aynı Unity sahnesinde iki ajan | Merge pratikte imkânsız |
| Yatay görev bölme | Her görev her dosyaya dokunur |
| Süresiz claim | Çöken ajan path'i sonsuza kilitler |
| Contract değişimini açık claim'lere bildirmemek | Ajan eski gerçeklikte çalışmaya devam eder |
| "Çakışırsa sonra çözeriz" | Semantik çakışma sonra görünmez |
