# 07 — Metrikler

> **Normatif rehber.** Bu bölüm ölçüm modelini ve kalibrasyon yöntemini tanımlar.
> Bir metriğin hedef repoda gerçekten gate olup olmadığı o reponun CI/ruleset
> ayarından doğrulanır.

Toplam satır coverage'ı tek başına kalite göstergesi veya merge gate'i değildir.
İstenirse tanı amaçlı tutulabilir; karar sinyali kriter, değişim ve mutation
kapsaması gibi davranışa yakın metriklerden gelir.

## 1. Hedef türleri

Metrikleri aynı tür eşik gibi ele alma:

| Tür | Kullanım | Örnek |
|---|---|---|
| **Değişmez (invariant)** | İhlali doğrudan hatadır; baseline beklemez | claim ihlali = 0, aktif AC referansı = %100 |
| **Kalibre gate** | Önce en az iki sprint baseline, sonra sürümlü repo eşiği | mutation, diff coverage, süre |
| **Gözlem** | Trend ve teşhis içindir; merge engellemez | escalation oranı, maliyet / AC |

Gate eşikleri repoda sürüm kontrollü, görünür ve lokal olarak yeniden
üretilebilir olmalıdır. “Gizli hedef” güvenlik kontrolü değildir.

---

## 2. Sadakat metrikleri

| Metrik | Başlangıç kullanımı | Neyi yakalar | Kaynak |
|---|---|---|---|
| **Kriter kapsaması** (aktif AC'lerin doğrulanmış test referansı) | **Değişmez: %100** | Spec drift | kapsama kontrolü ([`02` §2.1](02-spec-fidelity.md)) |
| **Mutation skoru** (diff, kritik modüller) | Baseline → repo eşiği | Sahte/boş testler | incremental mutation |
| **Harici gizli evaluator geçme oranı** | İzolasyon kurulunca baseline → repo eşiği | Görünür teste overfit / spec gaming | dış trust boundary |
| **Değişim kapsaması** (diff coverage) | Baseline → repo eşiği | Test edilmemiş ajan çıktısı | merge lane |
| **Geçersiz kırmızı kanıtı** | **Değişmez: 0** | Yanlış test, syntax/import hatasını kanıt sayma | [`06` §2](06-operations.md) |
| **Yeni testin başlangıçta yeşil olma oranı** | Gözlem; gerekçeye göre sınıflandır | Zaten var olan davranış veya zayıf oracle | [`06` §2](06-operations.md) |
| **Regresyon oranı** (merge sonrası kırılan test / PR) | Baseline → düşüş hedefi | Ajan kalite trendi | §6 |

---

## 3. Çakışma metrikleri

| Metrik | Başlangıç kullanımı | Neyi yakalar |
|---|---|---|
| **Merge sonrası kırılma oranı** | Baseline → düşüş hedefi | Eksik merge-group doğrulaması, semantik çakışma |
| **Aynı-dosya eşzamanlılık** | Gözlem → görev bölme bütçesi | Kötü görev bölme |
| **Merge conflict oranı** | Baseline → repo eşiği | Sahiplik ihlali, uzun branch ömrü |
| **Branch ömrü** | p50/p95 ölç → stack SLO'su | Çakışmanın öncü göstergesi |
| **Rebase / PR** | Gözlem | Aşırı paralellik |
| **Revert oranı** | Baseline → düşüş hedefi | Yakalanmamış semantik çakışma |
| **Claim ihlali** | **Değişmez: 0** | Protokol uyumu |
| **Invalidation gecikmesi** (contract/AC değişimi → etkilenen ajana bildirim) | Ölç → operasyon SLO'su | Eski gerçeklikte çalışan ajan |

---

## 4. Bütünlük metrikleri

| Metrik | Başlangıç kullanımı | Neyi yakalar |
|---|---|---|
| **Enforced fitness function ihlali** | **Değişmez: 0** | Mimari erozyon |
| **Diff'in getirdiği yeni duplikasyon** | Baseline → repo bütçesi | Yeniden-icat |
| **Bağımlılık sayısı değişimi** | Gözlem + gerekçe zorunluluğu | Şişme |
| **Gerekçesiz public sembol artışı** | **Değişmez: 0** | API yüzeyi sprawl |
| **Impact tahmin isabeti** | Baseline → iyileştirme | Kod grafı kalitesi |
| **Ölü kod trendi** | Gözlem → azalan trend | Birikim |
| **ADR'siz yapısal değişiklik** | **Değişmez: 0** | Görünmez karar |
| **Grounding kaydı olmayan PR** | Manuel kontrolken gözlem; enforcement sonrası 0 | Yeniden-icadın kaynağı |

---

## 5. Akış ve insan metrikleri

| Metrik | Başlangıç kullanımı | Neyi yakalar |
|---|---|---|
| **Fast lane süresi** (p95) | Ölç → stack'e özgü SLO | Ajan döngü hızı |
| **Merge lane süresi** (p95) | Ölç → repo SLO'su | Geri bildirim gecikmesi |
| **Flake oranı** | Baseline → düşüş hedefi | CI güvenilirliği |
| **Karantina TTL aşımı** | **Değişmez: 0** | Görmezden gelinen flake |
| **🔴 risk sınıfı PR oranı** | Gözlem | İnsan review yükünün sürdürülebilirliği |
| **İnsan review dakikası / merge edilmiş AC** | Gözlem → azalan trend | Sistemin gerçek ölçeklenmesi |
| **Escalation oranı** | Gözlem; başlangıçta hedef koyma | Ajan yetkinlik sınırı |
| **Çöpe giden iş oranı** | Baseline → düşüş hedefi | Reddedilen/terk edilen iş maliyeti |
| **Maliyet / merge edilmiş AC** | Gözlem → azalan trend | Ekonomik verim |

---

## 6. Regresyon oranı hedefi hakkında dürüst kayıt

v1.0 “regresyon oranı < %2” hedefini evrensel bir eşik gibi sunuyordu.
Dayandığı TDAD çalışmasındaki değerler şunlardı:

| | Değer |
|---|---|
| TDAD baseline (vanilla ajan) | %6.08 |
| TDAD + “TDD yap” prompt'u | %9.94 |
| TDAD + impact analysis | **%1.82** |

Bu sonuç belirli görev, model ve ölçüm düzenine aittir; bu repo veya başka bir
hedef repo için garanti değildir. Impact analysis mekanizması yine değerlidir
([`04` §5](04-codebase-integrity.md)), fakat eşik veri olmadan taşınamaz.

**Uygulama:** İlk iki sprint gate eşiği koymadan baseline ölç; örneklem sayısını,
model sürümünü, görev dağılımını ve ölçüm tanımını kaydet. Sonra hata maliyetine
ve ekip kapasitesine göre sürümlü eşik belirle. Aynı kural gizli evaluator,
mutation, diff coverage, süre ve flake oranları için de geçerlidir.

---

## 7. Metrik anti-pattern'leri

| ❌ | Neden |
|---|---|
| Toplam satır coverage'ını kalite özeti veya tek gate yapmak | Davranış ve oracle kalitesini göstermez |
| Test **sayısını** hedeflemek | Ajan sayıyı kolayca şişirir |
| Kapatılan görev veya PR sayısını başarı saymak | Rework ve çöpe giden işi gizler |
| Yazılan satır sayısını ödüllendirmek | Çürümeyi teşvik eder |
| Benchmark eşiğini doğrudan hedef repoya taşımak | Model, stack ve hata maliyetini yok sayar |
| Eşiği ajandan saklamak | Lokal yeniden üretimi engeller; güvenlik sınırı oluşturmaz |
| Yalnız eşik çevresindeki tek sayıyı izlemek | Goodhart etkisini ve dağılımı gizler |

Her gate adı, formülü, örneklem penceresi, istisnası ve eşik değişiklik geçmişiyle
birlikte görünür olmalıdır. Ajan sonucu ve nasıl yeniden üreteceğini görür; insan
ise trend dağılımını, eşik çevresindeki yığılmayı ve kaçış oranını ayrıca izler.
