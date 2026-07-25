# 07 — Metrikler

> **Normatif.** v1.0'da 5 metrik vardı ve hepsi spec sadakati eksenindeydi — repo'nun ilan ettiği ikinci amaç (çakışma) ve çürüme ekseni ölçülmüyordu.

**Birinci kural:** Toplam satır coverage'ı **dashboard'a bile koyma.** Ajanlı sistemde en yanıltıcı metrik odur.

---

## 1. Sadakat metrikleri

| Metrik | Hedef | Neyi yakalar | Kaynak |
|---|---|---|---|
| **Kriter kapsaması** (AC'lerin testli oranı; gizli manifest dahil) | %100 | Spec drift | [`tools/criteria_coverage.py`](../tools/criteria_coverage.py) |
| **Mutation skoru** (diff, kritik modüller) | ≥ %80 | Sahte/boş testler | incremental mutation, PR gate |
| **Gizli set geçme oranı** | ≥ %95 | Görünür teste overfit / spec gaming | merge queue |
| **Değişim kapsaması** (diff coverage) | ≥ %85 | Test edilmemiş ajan çıktısı | merge lane |
| **Kırmızı kanıtı başarısızlığı** (yeni testin baştan yeşil çıkma oranı) | < %5 | Hiçbir şey assert etmeyen test | [`06` §2](06-operations.md) |
| **Regresyon oranı** (merge sonrası kırılan test / PR) | < %2 | Ajan kalite trendi | ⚠ §5 |

---

## 2. Çakışma metrikleri

| Metrik | Hedef | Neyi yakalar |
|---|---|---|
| **Merge sonrası kırılma oranı** | < %1 | Merge queue eksikliği, semantik çakışma |
| **Aynı-dosya eşzamanlılık** (aynı dosyaya dokunan eşzamanlı açık PR oranı) | < %5 | Kötü görev bölme |
| **Merge conflict oranı** | < %10 | Sahiplik ihlali, uzun branch ömrü |
| **Ortalama branch ömrü** | < 8 saat | Çakışmanın öncü göstergesi |
| **Rebase / PR** | < 2 | Aşırı paralellik |
| **Revert oranı** | < %2 | Yakalanmamış semantik çakışma |
| **Claim ihlali** | 0 | Protokol uyumu |
| **Invalidation gecikmesi** (contract/AC değişimi → etkilenen ajana bildirim) | < 5 dk | Eski gerçeklikte çalışan ajan |

---

## 3. Bütünlük metrikleri

| Metrik | Hedef | Neyi yakalar |
|---|---|---|
| **Fitness function ihlali** | 0 | Mimari erozyon |
| **Diff'in getirdiği yeni duplikasyon** | < %3 | Yeniden-icat |
| **Bağımlılık sayısı değişimi** | net ≈ 0 | Şişme |
| **Gerekçesiz public sembol artışı** | 0 | API yüzeyi sprawl |
| **Impact tahmin isabeti** | > %80 | Kod grafı kalitesi |
| **Ölü kod trendi** | azalan | Birikim |
| **ADR'siz yapısal değişiklik** | 0 | Görünmez karar |
| **Grounding sorgusu olmayan PR** | 0 | Yeniden-icadın kaynağı |

---

## 4. Akış ve insan metrikleri

| Metrik | Hedef | Neyi yakalar |
|---|---|---|
| **Fast lane süresi** (p95) | < 3 dk | Ajan döngü hızı — otonom sistemde birincil kısıt |
| **Merge lane süresi** (p95) | < 12 dk | |
| **Flake oranı** | < %1 | CI güvenilirliği; ajana test zayıflatmayı öğreten şey |
| **Karantina TTL aşımı** | 0 | Görmezden gelinen flake |
| **🔴 risk sınıfı PR oranı** | < %20 | İnsan review yükü sürdürülebilir mi |
| **İnsan review dakikası / merge edilmiş AC** | azalan | Sistemin gerçek ölçeklenip ölçeklenmediği |
| **Escalation oranı** | ölç, hedef koyma | Ajan yetkinlik sınırı nerede |
| **Çöpe giden iş oranı** (reddedilen/terk edilen PR) | < %15 | Gerçek maliyet kalemi |
| **Maliyet / merge edilmiş AC** | azalan | |

---

## 5. ⚠ Regresyon oranı hedefi hakkında dürüst kayıt

v1.0 "regresyon oranı < %2" hedefi koymuştu. Bağlam:

| | Değer |
|---|---|
| TDAD baseline (vanilla ajan) | %6.08 |
| TDAD + "TDD yap" prompt'u | %9.94 |
| TDAD + impact analysis | **%1.82** |

Yani **< %2 hedefi, paper'ın state-of-the-art sonucudur** — ve v1.0 o sonucu üreten mekanizmayı (impact analysis) benimsememişti. Hedef, mekanizmasız olarak erişilemezdi.

Şimdi mekanizma benimsendi ([`04` §5](04-codebase-integrity.md)), ama:

- Ölçüm **küçük açık-ağırlık modellerde** yapıldı → [`01` §1.3](01-research.md)
- Frontier modellerin baseline'ı bilinmiyor — daha iyi de olabilir, farklı hata dağılımı da gösterebilir

**Doğru yaklaşım:** İlk 2 sprint hedef koymadan **kendi baseline'ını ölç.** Hedefi kendi verinden türet. Başkasının benchmark sayısını hedef olarak ithal etmek, bu dokümanın eleştirdiği "ölçmeden iddia" hatasının aynısıdır.

Aynı uyarı şunlar için de geçerli: gizli set geçme oranı ve mutation eşiği ([`01` §1.4](01-research.md) — analog domain'de ölçüldü).

---

## 6. Metrik anti-pattern'leri

| ❌ | Neden |
|---|---|
| Toplam satır coverage'ı takip etmek | Ajanlı sistemde en yanıltıcı sayı |
| Test **sayısını** takip etmek | Ajan istediğin kadar üretir; kalite sinyali sıfır |
| Kapatılan görev sayısı | Çöpe giden işi ve rework'ü gizler |
| Yazılan satır sayısı | Ters teşvik: çürümeyi ödüllendirir |
| PR sayısı | Aynı |
| Hedefi ajana metrik olarak vermek | Goodhart. Ajan metriği optimize eder, kaliteyi değil. **Metrikler insan içindir.** |

**Son kural:** Hiçbir gate eşiği ajanın system prompt'unda sayı olarak yazmaz. Ajan "mutation %80 olmalı" bilgisini alırsa %80'i hedefler. Gate'i CI uygular, ajan yalnız sonucu görür.
