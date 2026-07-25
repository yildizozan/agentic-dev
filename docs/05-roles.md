# 05 — Roller, Sahiplik ve İnsan Gate'leri

> **Normatif.** v1.0'a göre iki değişiklik: (a) Gherkin yazarlığı belirsizliği giderildi, (b) **insan gate'leri** eklendi — v1.0'da zincirde hiç insan yoktu.

---

## 1. Rol × sorumluluk matrisi

| Rol | Yazdığı artefakt | Sahip olduğu gate | **Yazması YASAK** |
|---|---|---|---|
| **PM / Producer** (ajan) | PRD, `AC-###` kabul kriterleri, Gherkin senaryo **taslağı**, DoD, kapsam sınırları | Kriter kapsaması | Test kodu, üretim kodu |
| **Tech Lead** (ajan) | Contract/şema, architecture fitness kuralları, `TESTING.md` taksonomisi, mutation eşiği, CI gate politikası, ownership-map | Contract diff, fitness function, mutation skoru, bağımlılık gate'i | Kabul kriteri (spec sahibi değil) |
| **Engineers** (Backend/Frontend/Mobile/Unity/Flutter) | Üretim kodu, unit + integration + property testleri, kendi modülünün replay testleri | Kendi PR'ının fast lane'i | **Acceptance testleri, regresyon çekirdeği, gizli set, contract** — dokunamaz |
| **Product Designer** (ajan + insan) | Design token sözleşmesi, golden baseline onayı, a11y kriterleri | Token diff, visual regression onayı | Fonksiyonel test |
| **QA** (ajan) | Acceptance test **otomasyonu**, E2E yolculuklar, gizli set, regresyon çekirdeği, flaky karantinası | Gizli set gate'i | Üretim kodu (bağımsızlık için) |
| **Security Engineer** (ajan) | Abuse-case senaryoları (negatif Gherkin), authz contract testleri, tehdit modeli türevli testler | SAST/SCA/secret/DAST | — |
| **`agent:deps`** | Bağımlılık ve lockfile değişiklikleri | Bağımlılık gate'i | Feature kodu |
| **`agent:migration`** | DB migration'ları | Migration PR'ı | Feature kodu |
| **İnsan (sen)** | Vizyon/constitution, **AC onayı**, mimari yön, risk kararları | **G1–G5** (§3) | — |

---

## 2. Gherkin yazarlığı — tek normatif cevap

v1.0'da üç yerde üç farklı şey yazıyordu (§2 diyagramı "QA yazar", §3 tablosu "PM yazar QA otomatize eder", §5 PM'e yalnız kriter veriyordu). Ayrık sahiplik load-bearing bir kontrol olduğu için bu belirsizlik kabul edilemezdi. Normatif akış:

| Adım | Kim | Çıktı |
|---|---|---|
| 1. Kabul kriterini ve Gherkin senaryo **taslağını** yaz | PM ajanı | `specs/acceptance-criteria/AC-###.md` |
| 2. **Onayla** | **İnsan (G1)** | Protected review/imzalı attestation + AC metadata'sı |
| 3. Onaylı Gherkin'i **çalıştırılabilir teste** çevir | QA ajanı | `tests/acceptance/**` |
| 4. Gizli varyantı yaz | Ayrı güven sınırındaki QA/evaluator | Harici oracle + görünür `tests/hidden/manifest.txt` |
| 5. Implementasyon | Engineer ajanı | `src/**` |

**Neden PM taslağı yazıyor, QA değil:** senaryo *spec'in kendisidir*. Spec sahibi PM'dir. QA'nın işi spec'i icat etmek değil, **çalıştırılabilir hale getirmek**.

**Neden QA otomatize ediyor, Engineer değil:** [`02` §4.1](02-spec-fidelity.md) — ajan geçeceği sınavı kendi yazmaz.

---

## 3. İnsan gate'leri — zincirin ground truth'u

### 3.1 Neden gerekli (v1.0'ın en derin açığı)

v1.0'ın pilot planında *"AC şablonu PM **ajanı** prompt'una gömülür"* yazıyordu. Yani:

```
AC'yi LLM yazıyor  →  testi başka LLM üretiyor  →  kodu üçüncü LLM yazıyor
                        →  review'ü dördüncü LLM yapıyor
```

Bu **kapalı bir döngüdür ve kendi içinde tutarlı biçimde yanlış olabilir.** Spec baştan eksik veya yanlışsa bütün gate'ler yeşil yanar; sistem kusursuz çalışırken yanlış ürünü üretir. v1.0'da insan yalnızca öznel "kullanım hissi" kabulü için bırakılmıştı.

**Çözüm:** insan dikkatini kodun *hacmine* değil, zincirin *dar boğazına* harca.

> **20 dakika AC okumak, 5.000 satır kod okumaktan hem ucuz hem daha etkilidir.** Çünkü AC yukarı akıştadır: oradaki bir hata aşağıdaki her şeyi yanlış yapar.

### 3.2 Gate listesi

| Gate | Ne | Kim | Maliyet | Neden insan |
|---|---|---|---|---|
| **G1** | **AC onayı** — feature başlamadan önce kabul kriterleri okunur ve protected review/imzalı attestation ile onaylanır | İnsan (ürün sahibi) | ~20 dk / feature | Zincirdeki tek ground truth. Frontmatter serbest metni tek başına kanıt değildir. |
| **G2** | **Risk-sıralı diff review** — kodun *tamamı* değil, riskli kısmı | İnsan | ~15 dk / PR | §3.3 |
| **G3** | **Breaking contract change** onayı | İnsan | ~5 dk | Geri dönüşü pahalı, çapraz-ajan etkili |
| **G4** | **Spec değişimi** onayı (AC v1 → v2) | İnsan | ~10 dk | Devam eden ajanları etkiler → [`06` §4](06-operations.md) |
| **G5** | **Kullanım hissi** kabulü (etkileşim tepkisi, akıcılık) | İnsan | değişken | Otomatikleştirilemez |

Ek: gizli test tahkimi (§4) ve model çelişkisinin spec yorumuna dayandığı durum ([`02` §4.8](02-spec-fidelity.md)) de insana gelir.

### 3.3 Risk-sıralı diff review (G2)

Premise: insan 5.000 satır okuyamaz. O yüzden **okumayacağını kabul et ve neyi okuyacağını seç.**

CI her PR'da diff'i risk sınıfına ayırır ve **yalnız yüksek risk hunk'larını** insana sunar:

| Risk | Tetikleyici | Aksiyon |
|---|---|---|
| 🔴 **Zorunlu insan okuması** | auth/authz, para/fiyat/vergi, PII, kriptografi, DB migration, silme/geri alınamaz işlem, concurrency/lock, public API yüzeyi, ownership-map/CI/CODEOWNERS değişikliği | İnsan okur, blocking |
| 🟡 **Özet + spot check** | yeni bağımlılık, yeni top-level dizin, fitness allowlist istisnası, > 400 satır dosya, ADR gerektiren karar | İnsan ADR + özeti okur |
| 🟢 **Gate'lere bırak** | geri kalan her şey | Otomatik |

Kural: **🔴 sınıf yoksa PR insan review'ü olmadan merge edilebilir.** Bu, insanı ölçeklenebilir kılan takas.

Sınıflandırma `ownership-map.yml`'deki `contention: high` etiketiyle ve path desenleriyle yapılır → [`templates/ownership-map.yml`](../templates/ownership-map.yml).

---

## 4. Tahkim: gizli test gerçekten hatalıysa

v1.0'da kapalı bir döngü vardı: QA üretim kodu yazamaz, Engineer gizli seti göremez → hatalı bir gizli test tüm hattı kilitler ve kimse çözemez.

Protokol:

```
1. Engineer ajanı "gizli test hatalı" iddiasında bulunur
   → İDDİA GEREKÇELİ OLMALI: hangi AC, hangi davranış, neden spec'e uygun
2. İddia insana (G1 sahibine) gider — QA ajanına DEĞİL
   (QA kendi testini savunmakta taraflıdır)
3. İnsan AC'yi okur ve karar verir:
   a) Spec bug   → AC güncellenir (v2) → spec-change protokolü → 06 §4
   b) Test bug   → QA ajanı gizli testi düzeltir, gerekçe kaydedilir
   c) Kod bug    → Engineer implement eder, iddia reddedilir
4. Karar ne olursa olsun kaydedilir. Aynı gizli testte 2. itiraz → test kalitesi sinyali
```

**Kural:** Gizli test itirazı ajanlar arası oylama ile çözülmez. Bir ajanın diğerinin sınavını geçersiz ilan etmesi, spec gaming'in en zarif biçimidir.

---

## 5. Ajan konfigürasyonu production artifact'tır

`CLAUDE.md`, `AGENTS.md`, skill dosyaları, subagent tanımları, system prompt'lar — bunlar **davranışı belirleyen kod**dur. v1.0 bunlardan yalnız `TESTING.md`'yi bir artefakt olarak anıyordu, genelleştirmiyordu.

| Kural | Detay |
|---|---|
| **Versiyonlanır** | Repoda, git'te. Ajanın lokal konfigürasyonuna güvenilmez. |
| **Review edilir** | Tech Lead sahibi. Prompt değişikliği kod değişikliğidir. |
| **Tek sahip** | `agent:techlead` → [`03` §1](03-concurrency.md) |
| **Değişiklik gerekçelidir** | "Ajan şunu yapmıyordu" → hangi PR'da hangi hata |
| **İdeal: eval'i olur** | Prompt değişiminin regresyon yaratmadığı ölçülür. Pilotta zorunlu değil, v2'de hedef. |

**Anti-pattern:** Feature ajanının kendi system prompt'unu / skill dosyasını aynı
feature kapsamında değiştirmesi. `CLAUDE.md`, `AGENTS.md`, `.claude/**` feature
ajanına kapalıdır. Değişiklik yalnız açık insan talebi/onayıyla, Tech Lead
sahipliğinde, ayrı governance kapsamı ve bağımsız kontrol testleriyle yapılır.
