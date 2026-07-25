---
adr: 0001
title: <karar, emir kipinde — "Postgres kullan", "Repository katmanı ekle">
status: proposed        # proposed | accepted | superseded | rejected
date: <YYYY-MM-DD>
deciders: [<ajan>, <insan — yapısal karar ise ZORUNLU>]
supersedes: ""
related_ac: []          # AC-### listesi
---

# ADR-0001 — <başlık>

> **Neden ADR zorunlu:** `docs/04-codebase-integrity.md` §8.
> Amaç dokümantasyon değil — **insanın 5.000 satır kod okumadan neyin değiştiğini
> anlaması.** ADR bir review yüzeyi küçültme aracıdır (`docs/05` §3.3 → 🟡 sınıf).
>
> ADR gerektiren değişiklikler: yeni top-level dizin · yeni bağımlılık kategorisi ·
> katman kuralı istisnası · yeni servis sınırı · veri modeli değişimi ·
> yeni async/queue mekanizması · fitness function allowlist istisnası.

## Bağlam

Hangi kısıt/problem bu kararı gerektirdi. Çözümü değil **zorlayıcı gerçeği** yaz.

## Karar

<Tek paragraf, net. "X yapacağız / Y kullanacağız.">

## Değerlendirilen alternatifler

| Alternatif | Neden seçilmedi |
|---|---|
| | |

> En az bir gerçek alternatif yaz. Alternatifsiz ADR karar değil, gerekçelendirmedir.

## Sonuçlar

**Kazandığımız:** <...>

**Kaybettiğimiz / kabul ettiğimiz maliyet:** <...>

**Geri dönüş maliyeti:** ☐ düşük ☐ orta ☐ yüksek (yüksekse insan onayı zorunlu)

## Mimari etki

- [ ] Katman kuralı değişti mi → `docs/04` §2 fitness function güncellenmeli
- [ ] Yeni bağımlılık var mı → `docs/04` §4.1 gate'i geçti mi
- [ ] Public API yüzeyi büyüdü mü → `docs/04` §4.2
- [ ] Yeni sahiplik domain'i gerekiyor mu → `templates/ownership-map.yml`
- [ ] Yeni yüksek çekişmeli dosya doğdu mu → `docs/03` §6

## Doğrulama

Bu kararın **çalıştırılabilir** karşılığı ne? (fitness function kuralı, contract testi, invariant)

> Doğrulaması olmayan ADR bir temennidir — bu repo'nun tezi tam olarak budur
> (`docs/02` §1). Karar bir kural üretmiyorsa neden ADR olduğunu sorgula.
