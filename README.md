# Agentic Otonom Geliştirme — Spec ve Best Practice Repo'su

> **Problem:** Ajanların yazdığı kodun tamamı okunmuyor; developer gitgide codebase'den kopuyor.
> Multi-agent kurulumda ajanlar birbirinin ayağına basıyor ve birbirinin değişikliğini bozuyor.
>
> **Bu repo:** o iki problemi **çalıştırılabilir kontrollere** çeviren kural seti.
>
> Versiyon: **v1.1** — 2026-07-25 · [v1.0'dan değişenler](#v10--v11-değişiklikler)

---

## TL;DR — beş cümle

1. **Spec tek başına yetmez.** Prose spec ajanın *niyetini* hizalar; sadakati sadece **çalıştırılabilir oracle** garanti eder.
2. **En yüksek kaldıraç** kabul kriteri ↔ test 1:1 eşlemesi ve contract testleridir — bunlar spec'in *kendisi* olur, spec *hakkında* bir belge olmaz.
3. **Asıl risk test eksikliği değil, test oyunlaştırmasıdır.** Ajan testi geçmek yerine testi değiştirmeyi öğrenir. Ayrık sahiplik + kilitli testler + gizli set + mutation durdurur.
4. **Contract testleri desync'i yakalar, çakışmayı önlemez.** Çakışma ayrı bir problem sınıfıdır: sahiplik + worktree izolasyonu + **merge queue** ile önlenir.
5. **Testler davranışı doğrular, yapı hakkında hiçbir şey söylemez.** Ajan tüm testleri geçerken codebase'i çürütebilir — bunu architecture fitness functions ve duplikasyon taraması yakalar.

---

## Üç eksen

Bu repo probleme üç ayrı eksenden bakar. Karıştırılmaları en yaygın hatadır:

| Eksen | Soru | Doküman |
|---|---|---|
| **Sadakat** | Ajan *istenen şeyi* yaptı mı? | [`02-spec-fidelity.md`](docs/02-spec-fidelity.md) |
| **Çakışma** | Ajanlar birbirini bozdu mu? | [`03-concurrency.md`](docs/03-concurrency.md) |
| **Bütünlük** | Codebase çürüdü mü? | [`04-codebase-integrity.md`](docs/04-codebase-integrity.md) |

> Yalnız birincisini çözmek yetmez. Bir ajan **her testi geçerken** hem başka bir ajanın
> işini bozabilir hem codebase'i çürütebilir. Üç eksen üç ayrı kontrol seti gerektirir.

---

## Repo haritası

```
docs/                     ← NORMATİF kurallar (stack-agnostik)
  01-research.md            araştırma bulguları + kaynaklar (tanımlayıcı)
  02-spec-fidelity.md       spec→test zinciri · 17 test türü · spec gaming'e karşı 9 kontrol
  03-concurrency.md         multi-agent çakışma protokolü · merge queue · çekişmeli dosyalar
  04-codebase-integrity.md  architecture fitness · duplikasyon · impact analysis · grounding
  05-roles.md               rol matrisi · İNSAN GATE'LERİ (G1–G5) · tahkim
  06-operations.md          CI şeritleri · kırmızı kanıtı · flake · spec değişimi · blast radius · escalation
  07-metrics.md             sadakat + çakışma + bütünlük + akış metrikleri
  08-pilot.md               1. hafta planı · başarı kriteri · baseline dönemi

templates/                ← KOPYALANABİLİR artefaktlar
  acceptance-criteria.md    AC-### şablonu (insan onay alanıyla)
  TESTING.md                ajan test taksonomisi skill dosyası
  ownership-map.yml         yazma sahipliği + risk sınıflandırma
  CODEOWNERS.example        + neden tek başına yetmediği
  gitattributes.example     çekişmeli dosya merge politikası (Unity dahil)
  spec-change.md            AC versiyon değişimi + invalidation bildirimi
  adr.md                    yapısal karar kaydı

tools/criteria_coverage.py  ← ÇALIŞAN checker: AC ↔ test eşlemesi + insan onayı
ci/pipeline.example.yml     ← üç şeritli referans pipeline
profiles/                   ← stack eşlemeleri: backend · flutter · unity
specs/acceptance-criteria/  ← AC'lerin yaşadığı yer (örnek AC dahil)
AGENTS.md                   ← ajan giriş noktası
```

---

## Hızlı başlangıç

```bash
# 1. Checker'ı çalıştır — repo kendi kuralını kendi üzerinde koşturur
python3 tools/criteria_coverage.py

# 2. Markdown rapor (PR yorumu için)
python3 tools/criteria_coverage.py --format markdown

# 3. Şablonları hedef repoya kopyala
cp templates/CODEOWNERS.example      <repo>/CODEOWNERS
cp templates/gitattributes.example   <repo>/.gitattributes
cp templates/TESTING.md              <repo>/TESTING.md      # <...> yerlerini doldur
cp templates/ownership-map.yml       <repo>/ownership-map.yml
cp ci/pipeline.example.yml           <repo>/.github/workflows/pipeline.yml
```

Kurulum sırası: [`docs/02` §5](docs/02-spec-fidelity.md) · Gün gün plan: [`docs/08`](docs/08-pilot.md)

---

## Pazarlıksız 10 kural

Geri kalan her şeyi atlarsan bunlar kalsın:

| # | Kural | Neden |
|---|---|---|
| 1 | **AC'yi insan onaylar** (G1) | Zincirdeki tek ground truth. AC'yi LLM yazıp testi LLM üretip kodu LLM yazarsa döngü **kendi içinde tutarlı biçimde yanlış** olabilir. |
| 2 | **`main`'e doğrudan push yok, merge queue zorunlu** | İki PR'ın izole halde yeşil olması merge sonrası yeşil olacağı anlamına gelmez. |
| 3 | **Kod ajanı acceptance/regresyon testine yazamaz** | Geçeceği sınavı kendi yazan ajan hizalanmış değildir. |
| 4 | **Kırmızı kanıtını CI üretir, ajan üretmez** | "Fabricated success reports" ölçülmüş bir ajan hata modudur (arXiv 2605.30777). |
| 5 | **Her path'in en fazla bir yazma sahibi vardır** | CODEOWNERS review ister, yazmayı engellemez — üçünü birlikte kur. |
| 6 | **Contract merge edilmeden paralel implementasyon başlamaz** | İki ajan iki farklı şema tasarlar, işin yarısı çöpe gider. |
| 7 | **Yazmadan önce ara** (grounding sorgusu zorunlu) | Aramayan ajan var olanı görmez, görmediğini yeniden yazar. Codebase'den kopmanın birincil mekanizması. |
| 8 | **Architecture fitness functions fast lane'de kırar** | Ajan tüm testleri geçerken mimariyi çürütebilir. |
| 9 | **Fast lane < 3 dk** | Otonom sistemde cycle time birincil kısıttır, gate sayısı değil. |
| 10 | **Gate eşikleri ajanın prompt'unda sayı olarak yazmaz** | Goodhart. Ajan sayıyı görürse sayıyı optimize eder. Metrikler insan içindir. |

---

## v1.0 → v1.1 değişiklikler

v1.0 tek dosyalık bir araştırma raporuydu. Değerlendirme sonucu yapılanlar:

### Düzeltilen iç tutarsızlıklar

| Sorun | Çözüm |
|---|---|
| Gherkin'i kim yazıyor? (üç yerde üç farklı cevap) | Normatif akış: PM taslak → **insan onay** → QA otomatize ([`05` §2](docs/05-roles.md)) |
| "Her AC'nin CI'da testi olmalı" ↔ gizli set görünmez | Gizli set **içerik sızdırmadan AC ID manifest'i** yayınlar; checker onu da okur ([`02` §2.1](docs/02-spec-fidelity.md)) |
| Mutation hem haftalık hem merge gate | PR'da **incremental** (gate) + haftalık tam suite (trend) ([`02` §4.4](docs/02-spec-fidelity.md)) |
| "Test yazan ajan ≠ kod yazan ajan" mutlak yazılmış ama Engineer test yazıyor | Kural **yalnız** acceptance/regresyon/gizli/contract için kapsamlandı ([`02` §4.1](docs/02-spec-fidelity.md)) |
| Kırmızı kanıtı PR artefaktı — ajan uydurabilir | **CI üretir**; kendi kaynakçasındaki 2605.30777 bunu zorunlu kılıyordu ([`06` §2](docs/06-operations.md)) |
| Hatalı gizli test tüm hattı kilitler, kimse çözemez | Tahkim protokolü ([`05` §4](docs/05-roles.md)) |
| Property-based "Bakım: 1" | Gerçekçi 2'ye çekildi; efor tahmini ayrıştırıldı |

### Eklenen bölümler (v1.0'da yoktu)

- **Multi-agent eşzamanlılık protokolü** — repo'nun ilan ettiği ikinci amaç yazılmamıştı: sahiplik, worktree izolasyonu, interface freeze sıralaması, claim/lease + TTL, merge queue, **yüksek çekişmeli dosya politikası** (lockfile · migration · generated · registry · **Unity sahne/prefab/meta**), semantik çakışma, görev bölme kuralları
- **Codebase bütünlüğü** — architecture fitness functions, duplikasyon taraması, bağımlılık gate'i, API surface diff, ölü kod bütçeleri, zorunlu grounding, ADR
- **İnsan gate'leri G1–G5** — v1.0'da zincirde hiç insan yoktu (yalnız öznel kullanım hissi kabulü); risk-sıralı diff review ile insan dikkatinin nereye harcanacağı tanımlandı
- **Operasyon** — üç şeritli CI (döngü süresi), flaky politikası, spec değişim protokolü + invalidation bildirimi, **ajan yetki sınırları / blast radius**, escalation ve durma koşulları, maliyet bütçesi
- **Çakışma + bütünlük + akış metrikleri** — v1.0'ın 5 metriği yalnız sadakat eksenindeydi
- **Çalıştırılabilir katman** — checker, CI pipeline, 7 şablon. v1.0 kendi tezine uymuyordu: "prose spec yetmez" diyen bir prose spec'ti.

### Kanıt katmanı düzeltmeleri

- Üç arXiv atfı doğrulandı (2603.17973, 2603.08806, 2605.30777) ve URL'lendi
- **Aynı isimli iki farklı TDAD paper'ı** ayrıştırıldı ([`01` §1.4](docs/01-research.md)); hidden split/mutation'ın kod ajanları için **doğrudan kanıtı olmadığı** açıkça kaydedildi
- "Ajanlara TDD yap demek zararlı" bulgusunun **küçük açık-ağırlık modellerde** ölçüldüğü kaydedildi; frontier modellere transferi kanıtlanmadığı için o sonuç benimsenmedi ([`01` §1.3](docs/01-research.md))
- **Impact analysis operasyonel hale getirildi** — dokümandaki kanıtı en güçlü müdahale (%70 regresyon düşüşü) v1.0'ın ROI listesinde, CI akışında ve pilot planında hiç geçmiyordu ([`04` §5](docs/04-codebase-integrity.md))
- Etki/Kurulum/Bakım sayılarının **ölçüm değil kalibre edilmiş yargı** olduğu belirtildi
- "Regresyon < %2" hedefinin paper'ın state-of-the-art sonucu olduğu ve mekanizmasız erişilemeyeceği kaydedildi; **hedefsiz baseline ölçüm dönemi** eklendi ([`07` §5](docs/07-metrics.md))
- Doğrulanamayan kaynaklar `⚠` ile işaretlendi + "tek gerekçe olarak kullanılamaz" kuralı

### Yapısal

- Tek 264 satırlık dosya → `docs/` (normatif) + `templates/` (kopyalanabilir) + `tools/` + `ci/` + `profiles/`
- **Tüm kurallar proje-agnostik hale getirildi.** `docs/` hiçbir somut projeye, ürüne veya domain'e atıf yapmaz; stack'e özgü her şey `profiles/` altında ve orada da yalnız teknoloji adıyla (Flutter, Unity, backend) anılır. Belirli bir ürün/proje adı repoda hiçbir yerde geçmez — geçerse hata sayılır (`profiles/README.md`).

---

## Bilinçli olarak yapılmayanlar

| Konu | Neden |
|---|---|
| Chaos/fault injection, screenshot visual regression | Efor/getiri oranı olgunlaşmadan kötü ([`08` §6](docs/08-pilot.md)) |
| Prompt/skill dosyaları için eval suite | v2 hedefi; önce temel gate'ler ([`05` §5](docs/05-roles.md)) |
| Hidden split / mutation eşiği için kesin hedef sayı | Kod ajanlarında ölçülmemiş — kendi baseline'ından türet ([`07` §5](docs/07-metrics.md)) |
| `⚠` kaynakların doğrulanması | Zaman; kural olarak tek gerekçe yapılamaz ([`01` §1.5](docs/01-research.md)) |
