# 04 — Codebase Bütünlüğü (Drift ve Çürüme Kontrolü)

> **Normatif.** Bu dosya v1.0'da yoktu.
> Kapsam: *"ajanın yazdığı kodu kimse okumuyor, codebase gitgide kopuyor"* probleminin **test dışı** ekseni.

---

## 0. Neden test yetmez

`02` davranışsal sadakati garanti eder. Ama:

> **Bir ajan test suite'inin %100'ünü geçerken codebase'i çürütebilir.**

Testler *davranışı* doğrular, *yapı* hakkında hiçbir şey söylemez. Ajan şunları yapıp yeşil kalabilir:

| Çürüme modu | Test ne der |
|---|---|
| Mevcut `formatCurrency`'i yeniden yazar (3. kopya) | ✅ Yeşil |
| Domain katmanından doğrudan HTTP çağırır (katman ihlali) | ✅ Yeşil |
| 4. HTTP client kütüphanesini ekler | ✅ Yeşil |
| İkinci bir auth kod yolu açar | ✅ Yeşil |
| Public API yüzeyini 40 sembol büyütür | ✅ Yeşil |
| Eski implementasyonu ölü bırakır, silmez | ✅ Yeşil |
| 900 satırlık bir dosya üretir | ✅ Yeşil |

Bunların hepsi **"codebase'den kopma"nın** ta kendisi. Ve hiçbiri test problemi değil. Bu dosya bunları çalıştırılabilir gate'lere çevirir.

---

## 1. Kontrol haritası

| # | Kontrol | Yakaladığı çürüme modu | Efor |
|---|---|---|---|
| 1 | Architecture fitness functions | Katman ihlali, döngüsel bağımlılık, paralel yol | 0.5–1 gün |
| 2 | Duplikasyon / benzerlik taraması | Yeniden-icat | 0.5 gün |
| 3 | Bağımlılık ekleme gate'i | Kütüphane şişmesi | 0.5 gün |
| 4 | Public API surface diff | Yüzey büyümesi | 0.5 gün |
| 5 | **Impact analysis (grounding + test seçimi)** | Sessiz regresyon | 0.5–1 gün |
| 6 | Ölü kod + boyut/karmaşıklık bütçesi | Birikim | 0.5 gün |
| 7 | Zorunlu index grounding (yazmadan önce ara) | Yeniden-icat, kaynağında | 0.5 gün |
| 8 | ADR zorunluluğu | Gerekçesiz yapısal karar | Sürekli |

---

## 2. Architecture fitness functions (ZORUNLU)

Mimariyi prose'dan çıkarıp **çalıştırılabilir kurala** çevirir. `02` §3'te test türü #4; efor olarak statik kapı kadar ucuz, etki olarak contract testleri kadar yüksek.

### 2.1 Kurallar

Minimum kural seti — her repo bunları tanımlar:

```
1. Katman yönü        : domain ← application ← infrastructure ← ui
                        (domain hiçbir şeye bağımlı olamaz)
2. Yasak import       : domain/** içinden http/db/framework import YASAK
3. Döngüsel bağımlılık: sıfır tolerans
4. Modül sınırı       : feature modülleri birbirini doğrudan import etmez,
                        yalnız ortak arayüz üzerinden
5. Allowlist          : yeni top-level dizin eklemek onay gerektirir
```

### 2.2 Araçlar

| Stack | Araç |
|---|---|
| TS/JS | `dependency-cruiser`, `eslint-plugin-boundaries` |
| Python | `import-linter`, `pytest-archon` |
| Dart/Flutter | `dart_code_metrics` (banned imports), custom `analysis_options.yaml` lint |
| C#/Unity | `NetArchTest`, asmdef referans kısıtları (Unity'de assembly definition **doğal** fitness function'dır — kullan) |
| JVM | `ArchUnit` |
| Go | `go-arch-lint`, `depguard` |
| Ruby | `packwerk` |

### 2.3 Kural

> Fitness function ihlali **fast lane'de** kırar (< 30 sn). Uyarı değil, hata. İhlal gerekiyorsa ADR + Tech Lead onayı ile allowlist'e eklenir; sessiz istisna yoktur.

---

## 3. Duplikasyon / benzerlik taraması (ZORUNLU)

Ajanların en sık ve en görünmez çürüme davranışı: **var olanı yeniden yazmak.** [`03` §7.1](03-concurrency.md)'deki semantik çakışmanın tespit katmanı.

| Katman | Araç | Gate |
|---|---|---|
| Token bazlı | `jscpd`, `PMD CPD`, `simian` | Yeni duplikasyon bloğu (> 30 satır) → PR uyarısı + gerekçe zorunlu |
| Yapısal | AST benzerliği | Aynı imzalı yeni fonksiyon → **kırar** |
| Semantik | Embedding benzerliği (codebase index) | Benzerlik > eşik → ajana "şu zaten var" uyarısı |

**Pratik kural:** Mutlak duplikasyon oranı gate'lemek gürültülüdür. **Diff'in getirdiği yeni duplikasyonu** gate'le — `03`'ün diff-coverage mantığıyla aynı.

---

## 4. Bağımlılık ekleme gate'i ve API surface diff (ZORUNLU)

### 4.1 Bağımlılık gate'i

Şişmenin girdiği kapı burasıdır. Ajan bir kütüphane ekliyorsa PR'da şunlar zorunlu:

- Neden mevcut bağımlılıklarla çözülemiyor
- Lisans + bakım durumu (son commit, açık CVE)
- Boyut etkisi (bundle/APK)
- **`agent:deps` sahibinin onayı** → [`03` §6](03-concurrency.md)

Otomatik red koşulları: allowlist dışı lisans, kritik CVE, 12 aydır commit yok, aynı işi yapan bir bağımlılık zaten var.

### 4.2 Public API surface diff

Her PR'da dışa açık sembol yüzeyinin diff'i raporlanır (`api_extractor`, `.api` dump, `public_api` snapshot).

> **Kural:** Yüzey büyümesi *sessiz* olamaz. Yeni public sembol → PR'da tek satır gerekçe. Gerekçesiz büyüme, ajanın "her şeyi export et" eğiliminin imzasıdır.

---

## 5. Impact analysis — bu repodaki kanıtı en güçlü müdahale (ZORUNLU)

### 5.1 Neden birinci sınıf

Ölçülmüş sonuç: kod–test grafı üzerinden ajana **hangi testleri kontrol edeceğini** söylemek regresyonu **%70 düşürüyor** (%6.08 → %1.82, arXiv 2603.17973).

> **v1.0'ın en büyük operasyonel açığı buydu:** bu bulgu araştırma tablosunda bir satır olarak duruyor, ama ROI sıralamasında, CI akışında ve pilot planında **hiç geçmiyordu.** Dokümanın kendi kaynakçasındaki en kanıtlı şey, kendi eylem planında yoktu.
>
> Üstüne: v1.0 metrik hedefi "regresyon oranı < %2" koymuş. Paper'ın baseline'ı %6.08, mekanizmayla ulaştığı yer %1.82. Yani **mekanizmayı benimsemeden paper'ın state-of-the-art sonucu hedeflenmişti.**

⚠ Geçerlilik sınırı (küçük açık-ağırlık modellerde ölçüldü) → [`01` §1.3](01-research.md). Mekanizmayı benimsiyoruz; "ajana TDD anlatma" sonucunu benimsemiyoruz.

### 5.2 Uygulama

```
ajan değişiklik yapmadan ÖNCE:
  1. Dokunacağı sembolleri belirle
  2. Kod–test grafından etkilenen testleri çıkar
  3. Bu listeyi PR gövdesine yaz
  4. Fast lane'de yalnız bu testleri koş   → hem doğruluk hem hız

CI merge lane:
  5. Tam suite (queue içinde)
  6. Ajanın çıkardığı liste ile gerçekte kırılan testleri karşılaştır
     → fark, impact grafının kalitesi hakkında metrik
```

### 5.3 Araç

- Referans implementasyon: TDAD (AST tabanlı kod–test grafı, ajan skill dosyası olarak sunulur)
- Bu ortamda hazır: `codebase-memory-mcp` → `trace_path(mode=calls)`, `search_graph`, `query_graph`. Kod grafı zaten var; eksik olan **ajan iş akışına gate olarak bağlanması**.
- Dil-agnostik ucuz alternatif: coverage verisinden test↔dosya haritası üretmek (`pytest-testmon`, `jest --findRelatedTests`, `dotnet-affected`)

---

## 6. Ölü kod ve bütçeler (ZORUNLU)

| Kontrol | Eşik | Not |
|---|---|---|
| Erişilemez kod | 0 yeni | `knip`, `vulture`, `ts-prune`, Roslyn analyzer |
| Öksüz test | 0 | Sildiği koda ait test kalmışsa |
| Dosya boyutu | yeni dosya < 400 satır | Aşımda gerekçe |
| Fonksiyon karmaşıklığı | cyclomatic < 15 | |
| Yeni top-level dizin | onay gerekli | Yapısal karar → ADR |

**Kural:** Ajan bir implementasyonu değiştirdiğinde eskisini **silmek zorundadır.** "İhtiyaten bırakalım" ajan çürümesinin en yaygın biçimidir; bir insan review'ü olmadığı için asla geri dönülüp temizlenmez.

---

## 7. Zorunlu grounding — yazmadan önce ara (ZORUNLU)

Yeniden-icadı **tespit** etmek yerine **önlemek**. En ucuz kontrol, en yüksek etki.

Ajan iş akışına gömülü zorunlu adım:

```
Yeni bir fonksiyon/servis/util yazmadan önce:
  1. search_graph(name_pattern=<niyet>)        → aynı isimli var mı
  2. search_code(<davranış anahtar kelimesi>)  → aynı iş yapan var mı
  3. get_architecture()                        → bu hangi katmana ait
  4. Bulduysan: KULLAN veya GENİŞLET. Yeni yazacaksan PR'da neden yazdığını belirt.
```

Bu adım ajanın system prompt'una / skill dosyasına girer, "iyi olur" tavsiyesi olarak değil **çıktı şartı** olarak: PR gövdesinde grounding sorgusu sonucu yoksa PR reddedilir.

> Gerekçe: rehbersiz ajan repodaki baskın deseni kopyalar ([`01` §1.1](01-research.md)). Aramadığı için var olanı görmez; görmediği için yeniden yazar. Bu, codebase'den kopmanın birincil mekanizmasıdır.

---

## 8. ADR zorunluluğu (ZORUNLU)

Yapısal karar veren her değişiklik ADR gerektirir: yeni top-level dizin, yeni bağımlılık kategorisi, katman kuralı istisnası, yeni servis sınırı, veri modeli değişimi, yeni async/queue mekanizması.

Şablon: [`templates/adr.md`](../templates/adr.md). Bu ortamda `codebase-memory-mcp → manage_adr` mevcut.

Amaç dokümantasyon değil: **insanın 5.000 satır kod okumadan neyin değiştiğini anlaması.** ADR, review yüzeyini küçültme aracıdır → [`05` §3.2](05-roles.md).

---

## 9. Bütünlük metrikleri

[`07`](07-metrics.md)'ye eklenenler:

| Metrik | Hedef | Neyi yakalar |
|---|---|---|
| Fitness function ihlali | 0 | Mimari erozyon |
| Diff'in getirdiği yeni duplikasyon | < %3 | Yeniden-icat |
| Bağımlılık sayısı değişimi | net ≈ 0 | Şişme |
| Gerekçesiz public sembol artışı | 0 | Yüzey sprawl |
| Impact tahmin isabeti (tahmin edilen ÷ gerçekte kırılan test) | > %80 | Kod grafı kalitesi |
| Ölü kod trendi | azalan | Birikim |
| ADR'siz yapısal değişiklik | 0 | Görünmez karar |
