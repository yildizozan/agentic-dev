# harness/ — `AGENTS.md` yazacaksan buradasın

Bu kol **proje kapsamlı** kuralları üretir: ajanın bu repoda ne yapacağı, neye
dokunamayacağı, hangi komutu koşacağı.

Geçerli olduğu ortamlar: **Claude Code · Codex · Cursor · Hermes** — hepsi
`AGENTS.md` okur.

---

## 👉 Tek adım

**[`AGENTS.template.md`](AGENTS.template.md)** → kopyala, `<...>` yerlerini doldur,
kendi projenin köküne **`AGENTS.md`** olarak koy.

```
Seviye 1  → tek ajan (7 kural, ~40 satır). Bununla başla.
Seviye 2  → aynı repoda birden fazla ajan (sahiplik, worktree, merge)
```

Şablon tek başına çalışır; başka hiçbir dosyayı okuman gerekmez.

---

## Hermes kullanıyorsan bu kol da senin

Yaygın yanlış anlama: "Hermes'te `SOUL.md` var, `AGENTS.md`'ye gerek yok."
Hermes'in kendi dokümanı tersini söylüyor — **ikisini birlikte okur** ve ayrımı
şöyle koyar:

> *"if it should follow you everywhere, it belongs in `SOUL.md`;
> if it belongs to a project, it belongs in `AGENTS.md`"*
> — [Hermes: Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)

Aynı doküman `SOUL.md` için açıkça şunu **kapsam dışı** bırakıyor:
*"one-off project instructions, file paths, repo conventions, temporary workflow
details. Those belong in `AGENTS.md`, not `SOUL.md`."*

| | `AGENTS.md` (bu kol) | `SOUL.md` ([`../hermes/`](../hermes/)) |
|---|---|---|
| Kapsam | **Proje** — repo ile birlikte yaşar | **Ajan** — her yere seninle gider |
| İçerik | Komutlar, path'ler, dokunma yasakları, iş akışı | Ses, tonu, kararsızlıkta/itirazda davranış |
| Nerede durur | Proje kökü | `~/.hermes/profiles/<ad>/SOUL.md` |
| Değişme sıklığı | Proje değişince | Nadiren |

**Kısaca:** Hermes kullanıcısı `SOUL.md` **ve** `AGENTS.md` yazar. Proje kuralını
`SOUL.md`'ye koymak, onu tüm projelere bulaştırır.

---

## Derinleştirmek istersen

Şablonu koyup bir hafta kullandıktan sonra sorun çıkan maddeyi derinleştir.
Sırası önemli — hepsini birden kurma:

| Sorun gördüysen | Buraya git |
|---|---|
| Ajan test dizinine dokunuyor, testi zayıflatıyor | [`../docs/02-spec-fidelity.md`](../docs/02-spec-fidelity.md) |
| İki ajan birbirini bozuyor, merge çakışıyor | [`../docs/03-concurrency.md`](../docs/03-concurrency.md) |
| Codebase çürüyor, aynı şey ikinci kez yazılıyor | [`../docs/04-codebase-integrity.md`](../docs/04-codebase-integrity.md) |
| Kim neyi onaylıyor belirsiz | [`../docs/05-roles.md`](../docs/05-roles.md) |
| CI yavaş, flake var, ajan takılınca ne olacak | [`../docs/06-operations.md`](../docs/06-operations.md) |
| Neyi ölçeceğimi bilmiyorum | [`../docs/07-metrics.md`](../docs/07-metrics.md) |

## Yardımcı şablonlar (opsiyonel)

`AGENTS.md` yetmediğinde projeye eklenebilecek dosyalar:

| Dosya | Ne zaman |
|---|---|
| [`../templates/TESTING.md`](../templates/TESTING.md) | Ajan yanlış katmanda test yazıyorsa |
| [`../templates/CODEOWNERS.example`](../templates/CODEOWNERS.example) | Review sahipliği gerekiyorsa |
| [`../templates/gitattributes.example`](../templates/gitattributes.example) | Lockfile/generated/Unity dosyaları çakışıyorsa |
| [`../templates/ownership-map.yml`](../templates/ownership-map.yml) | 3+ ajan paralel çalışıyorsa |
| [`../templates/acceptance-criteria.md`](../templates/acceptance-criteria.md) | Kabul kriterini yazılı hale getireceksen |
| [`../templates/adr.md`](../templates/adr.md) · [`../templates/spec-change.md`](../templates/spec-change.md) | Yapısal karar · spec değişimi |

## Stack eşlemeleri

Somut araç isimleri: [`../stacks/backend.md`](../stacks/backend.md) ·
[`../stacks/flutter.md`](../stacks/flutter.md) ·
[`../stacks/unity.md`](../stacks/unity.md)
