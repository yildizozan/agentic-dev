# Agentic Development — Saha Rehberi

Ajanlarla (Claude Code, Codex, Cursor…) yazılım geliştirirken kodun tamamı
okunmuyor, codebase zamanla kopuyor ve birden fazla ajan birbirinin işini
bozuyor. Bu repo bunun için **ne yapacağını** anlatır.

## 👉 Buradan başla

**Projendeki ajanlara ne söyleyeceğini arıyorsan** → **[`templates/AGENTS.md`](templates/AGENTS.md)**

Kopyala-yapıştır tek dosya. Kendi projenin köküne `AGENTS.md` olarak koy,
`<...>` yerlerini doldur, bitti. Başka hiçbir şey okumana gerek yok.

```
Seviye 1  → tek ajanla çalışıyorsan (7 kural, ~40 satır). Bununla başla.
Seviye 2  → birden fazla ajan aynı repoda çalışıyorsa (sahiplik, worktree, merge)
```

Gerisi **neden** bölümü. Bir kuralın gerekçesini, kanıtını veya ölçümünü merak
ettiğinde `docs/` altına gel — `AGENTS.md` yazmak için gerekmez.

<details>
<summary>Bu repo ne <b>değil</b>?</summary>

Framework, policy motoru veya çalıştırılacak bir uygulama değil. Ürün; kaynakları
açık, sınırlılıkları dürüst ve kendi repona uyarlanabilir **rehber içeriği**.
Kurulacak bir şey yok; kopyalanacak şablonlar ve okunacak gerekçeler var.

Son araştırma güncellemesi: **2026-07-25** ·
yöntem: [Web + Reddit Saha Rehberi](docs/09-web-reddit-field-guide.md)
</details>

---

## Ne problemi çözüyor?

Rehber üç ayrı riski birbirine karıştırmadan ele alır:

| Eksen | Soru | Ana bölüm |
|---|---|---|
| **Sadakat** | Ajan istenen davranışı gerçekten üretti mi? | [Spec sadakati](docs/02-spec-fidelity.md) |
| **Eşzamanlılık** | Paralel ajanlar birbirinin işini bozdu mu? | [Çakışma](docs/03-concurrency.md) |
| **Bütünlük** | Değişiklik codebase'i zamanla çürütüyor mu? | [Codebase bütünlüğü](docs/04-codebase-integrity.md) |

Test, contract, worktree, merge queue, ownership ve benzeri yapılar bu rehberin
**hedef kod repoları için değerlendirdiği araçlardır**. Bu rehber reposunun
kendisinde aynı altyapıların kurulması zorunlu değildir.

## Rehberi nasıl kullanırsın?

**Kısa yol (çoğu kişi buraya kadar):**

1. [`templates/AGENTS.md`](templates/AGENTS.md)'i kopyala, doldur, projenin köküne koy.
2. Bir hafta kullan. Üç şeyi say: ajan kapalı test dizinine dokunmaya çalıştı mı,
   "bitti" deyip bitirmedi mi, iki ajan aynı dosyada çakıştı mı.
3. Sorun çıkan maddeyi derinleştir — aşağıdaki uzun yol.

**Uzun yol (bir kuralın nedenini veya ölçümünü arıyorsan):**

4. İhtiyacına göre sadakat, eşzamanlılık veya bütünlük bölümüne git (yukarıdaki tablo).
5. [Roller](docs/05-roles.md), [operasyon](docs/06-operations.md) ve
   [metrikler](docs/07-metrics.md) ile öneriyi kendi organizasyonuna uyarla.
6. [Pilot planı](docs/08-pilot.md) ile küçük bir deneme yap; evrensel eşik
   kopyalamak yerine kendi baseline'ını ölç.
7. Rehbere katkı yapacaksan [web + Reddit araştırma yöntemini](docs/09-web-reddit-field-guide.md)
   uygula. [Kanıt sınırları](docs/01-research.md) burada.

## Repo haritası

```text
templates/
  AGENTS.md                 ★ ARADIĞIN ŞEY BU — kopyala-yapıştır, tek dosya
  TESTING.md                  test taksonomisi (ajana test kuralı vermek istersen)
  CODEOWNERS.example          sahiplik/review
  gitattributes.example       çakışan dosya merge politikası
  ownership-map.yml           çok ajanlı sahiplik haritası
  acceptance-criteria.md      kabul kriteri şablonu
  adr.md · spec-change.md     karar kaydı · spec değişimi

docs/                       ← "neden" bölümü, AGENTS.md yazmak için gerekmez
  01-research.md              araştırma bulguları ve kaynak sınırları
  02-spec-fidelity.md         spec, oracle ve test-gaming riskleri
  03-concurrency.md           ownership, worktree, lease ve merge queue
  04-codebase-integrity.md    mimari erozyon, impact analysis, grounding
  05-roles.md                 ajan ve insan sorumlulukları
  06-operations.md            operasyon, güvenlik sınırı, escalation
  07-metrics.md               invariant, kalibre gate ve gözlemsel metrikler
  08-pilot.md                 aşamalı pilot önerisi
  09-web-reddit-field-guide.md
                              dış bulgu → sınırlılık → rehber kararı

profiles/                   stack eşlemeleri: backend · Flutter · Unity
ci/, tools/, specs/, tests/ hedef repo örnekleri (bu repoda kurulu değil)
AGENTS.md                   bu REHBERE katkı yapan ajanlar için
                            (projendeki ajanlar için olan → templates/AGENTS.md)
```

> `AGENTS.md` ile `templates/AGENTS.md` karıştırılmasın: ilki bu rehber
> repo'sunda çalışan ajanı, ikincisi **senin projendeki** ajanı yönetir.

`profiles/`, `templates/`, `ci/`, `tools/`, `specs/` ve `tests/` altındaki
artefaktlar “bu repoda kurulması gereken mimari” değildir. Bunlar yalnız hedef
kod repolarında tartışılan pratikleri somutlaştıran örneklerdir.

## Kanıt hiyerarşisi

| Sınıf | Ne söyler? | Sınırı |
|---|---|---|
| **Resmi/primary kaynak** | Araç davranışı ve güvenlik semantiği | Organizasyonundaki kurulumun gerçekten aktif olduğunu kanıtlamaz |
| **Ampirik araştırma** | Belirli deney düzenindeki ölçüm | Başka model/stack için evrensel sonuç değildir |
| **Reddit saha sinyali** | Gerçek kullanıcıların yaşadığı olası failure mode | Prevalans ve nedensellik göstermez |
| **Rehber önerisi** | Kanıt, risk ve maliyet sentezi | Hedef repoda pilot ve uyarlama ister |

Reddit araştırması bilinçli olarak kullanılır; gönderiler normatif kanıt değil,
ölçülmesi gereken hipotez ve ergonomi riski üretir.

## Çekirdek öneriler

- Prose spec'i başarı raporu sanma; doğrulanabilir davranışı açık oracle veya
  insan kabulüyle bağla.
- Kritik oracle ile implementasyon yetkisini risk oranında ayır.
- `CODEOWNERS` review mekanizmasıdır; aktif write lease veya push kilidi değildir.
- Paralel ajanları ayrı çalışma alanında çalıştır; worktree'nin runtime, port,
  secret veya semantik merge izolasyonu sağlamadığını unutma.
- Merge queue kullanıyorsan required kontrolleri birleşik `merge_group` state'inde
  yeniden çalıştır.
- PR kontrollü kodu secret veya hidden oracle ile aynı trust boundary'de
  çalıştırma.
- Lockfile/generated/registry politikasını stack'e göre seç; `ours/union` gibi
  metinsel merge tercihini semantik doğrulama yerine koyma.
- Benchmark yüzdelerini doğrudan eşik yapma; önce hedef repoda baseline ölç.
- Ajanın “bitti” raporunu dış kanıt sayma; tamamlanma sinyalini görev türüne göre
  açıkça tanımla.
- Üretim hızıyla birlikte review dakikası, rework, revert ve ölü kod trendini de
  izle.

Bu maddelerin kanıt bağlantıları ve sınırlılıkları
[saha rehberinde](docs/09-web-reddit-field-guide.md) bulunur.

## Bu rehber nasıl güncellenir?

Her anlamlı içerik değişikliğinde:

1. Resmi/primary web taraması yapılır.
2. Aynı konu Reddit'te aranır.
3. Sorgu ve erişim tarihi kaydedilir.
4. Resmi bulgu ile Reddit anekdotu ayrı etiketlenir.
5. Çelişen bulgular ve transfer sınırları yazılır.
6. Lokal Markdown linkleri ve `git diff --check` doğrulanır.

Rehber katkısı için kod testi veya TDD akışı gerekmez. Doğrulama; kaynak
izlenebilirliği, link bütünlüğü, terminoloji tutarlılığı ve eleştirel sentezdir.

## Bilinçli sınırlılıklar

- Rehber, hedef repodaki branch protection veya CI ayarlarını uzaktan doğrulamaz.
- Reddit örneklerinin temsil gücü yoktur.
- Akademik sonuçlar hızlı değişen model/harness ekosistemine otomatik transfer
  edilmez.
- Stack profilleri başlangıç noktasıdır; her projeye aynen uygulanmaz.
- Kesin eşikler yerine pilot ve baseline yaklaşımı kullanılır.
