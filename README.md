# Agentic Development — Araştırma Destekli Saha Rehberi

Bu repo, tek ve çok ajanlı yazılım geliştirme süreçlerini daha güvenli,
denetlenebilir ve sürdürülebilir kurmak için hazırlanmış bir **Markdown
rehberidir**.

> Bu repo bir framework, policy motoru veya örnek uygulama değildir. Kendi
> doğruluğunu TDD, self-CI ya da makine-okunur gate'lerle kanıtlamaya çalışmaz.
> Buradaki ürün; kaynakları açık, sınırlılıkları dürüst ve hedef repoya
> uyarlanabilir rehber içeriğidir.

Son araştırma güncellemesi: **2026-07-25**

Başlangıç noktası: [Web + Reddit Saha Rehberi](docs/09-web-reddit-field-guide.md)

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

1. [Araştırma bulguları](docs/01-research.md) ile kanıt sınırlarını oku.
2. İhtiyacına göre sadakat, eşzamanlılık veya bütünlük bölümüne git.
3. [Roller](docs/05-roles.md), [operasyon](docs/06-operations.md) ve
   [metrikler](docs/07-metrics.md) ile öneriyi kendi organizasyonuna uyarla.
4. [Pilot planı](docs/08-pilot.md) ile küçük bir deneme yap; evrensel eşik
   kopyalamak yerine kendi baseline'ını ölç.
5. Yeni karar verirken [web + Reddit araştırma yöntemini](docs/09-web-reddit-field-guide.md)
   uygula.

## Repo haritası

```text
docs/
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

profiles/                     backend, Flutter ve Unity eşlemeleri
templates/                    hedef repoya uyarlanabilecek örnek belgeler/config
ci/, tools/, specs/, tests/   opsiyonel tarihsel/hedef-repo örnekleri
AGENTS.md                     korumalı ajan giriş noktası; README haritasına yönlendirir
```

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
