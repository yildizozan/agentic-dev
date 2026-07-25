---
id: AC-001
title: Kısa, davranış odaklı başlık
version: 1
status: active            # active | superseded
supersedes: ""            # önceki versiyonun AC ID'si (varsa)
hidden: false             # true ise gizli sette varyantı olmalı (docs/02 §4.3)
approved: false           # ⚠ İNSAN doldurur — G1 (docs/05 §3.2)
approved_by: ""           # insan adı/handle. Ajan bu alanı DOLDURAMAZ.
approved_at: ""           # YYYY-MM-DD
owner_domain: ""          # ownership-map.yml'deki domain (docs/03 §1)
risk: normal              # normal | high  → high ise G2 zorunlu (docs/05 §3.3)
---

# AC-001 — <başlık>

> **Kural:** `approved: true` olmadan bu AC'ye karşı implementasyon başlamaz.
> `criteria_coverage.py` onaysız aktif AC'de build'i kırar.

## Bağlam

Bir paragraf: hangi kullanıcı problemi, neden şimdi. Çözümü değil problemi yaz.

## Kabul senaryoları (Gherkin)

PM ajanı taslağı yazar → **insan onaylar** → QA ajanı çalıştırılabilir teste çevirir.
Her senaryo testte `AC-001` etiketi taşımak ZORUNLUDUR (docs/02 §4.6).

```gherkin
Feature: <özellik>

  Scenario: <mutlu yol — tek, net davranış>
    Given <başlangıç durumu, gözlemlenebilir>
    When <tek eylem>
    Then <tek doğrulanabilir sonuç>

  Scenario: <sınır durumu>
    Given ...
    When ...
    Then ...
```

## Negatif senaryolar (ZORUNLU)

Security ajanı buraya abuse-case ekler. En az bir tane olmalı — "ne olmamalı"
yazılmayan AC, ajanın en geniş yorumu yapmasına izin verir.

```gherkin
  Scenario: Yetkisiz kullanıcı erişemez
    Given <başka kullanıcının kaynağı>
    When <erişim denemesi>
    Then <403, ve kaynak sızmaz>
```

## Ölçülebilir kısıtlar

Spec'te sayı varsa o bir kabul kriteridir ve ölçülmelidir (docs/02 §3.13).

| Kısıt | Değer | Nasıl ölçülür |
|---|---|---|
| p95 latency | < 200 ms | k6 |
| frame time | < 16.6 ms | profiler marker |

Yoksa: `yok`.

## Kapsam dışı (ZORUNLU)

Açıkça yapılmayacaklar. Bu bölüm boş bırakılamaz — ajanın kapsamı kendi
genişletmesini engelleyen tek şey budur (docs/06 §6.3).

- ...

## Definition of Done

- [ ] Acceptance test yazıldı ve `AC-001` etiketi taşıyor
- [ ] CI kırmızı kanıtını üretti (docs/06 §2)
- [ ] Negatif senaryoların testi var
- [ ] Ölçülebilir kısıtlar ölçülüyor
- [ ] Diff coverage ≥ %85, incremental mutation ≥ %80
- [ ] Grounding sorgusu PR'da (docs/04 §7)
- [ ] Impact analizi PR'da (docs/04 §5)
- [ ] `risk: high` ise G2 insan review'ü yapıldı

## Değişiklik geçmişi

| Versiyon | Tarih | Değişiklik | Onaylayan |
|---|---|---|---|
| 1 | | ilk | |
