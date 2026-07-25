# harness/ — `AGENTS.md` yazacaksan buradasın

**Proje kapsamlı** kurallar: ajanın bu repoda ne yapacağı, neye dokunamayacağı,
hangi komutu koşacağı.

Geçerli olduğu ortamlar: **Claude Code · Codex · Cursor · Hermes** — hepsi
`AGENTS.md` okur.

## 👉 Tek adım

**[`AGENTS.template.md`](AGENTS.template.md)** → kopyala, `<...>` yerlerini doldur,
kendi projenin köküne **`AGENTS.md`** olarak koy.

```
Seviye 1  → tek ajan (7 kural, ~40 satır). Bununla başla.
Seviye 2  → aynı repoda birden fazla ajan (sahiplik, worktree, merge)
```

Şablon tek başına çalışır. Doldurmadığın satırı **sil** — `<...>` bırakılmış bir
kural, kural değildir; ajan onu atlar.

## Hermes kullanıyorsan bu kol da senin

"Hermes'te `SOUL.md` var, `AGENTS.md`'ye gerek yok" yaygın bir yanlış anlama.
Hermes **ikisini birlikte okur** ve ayrımı şöyle koyar:

> *"if it should follow you everywhere, it belongs in `SOUL.md`;
> if it belongs to a project, it belongs in `AGENTS.md`"*
> — [Hermes: Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)

Aynı doküman `SOUL.md` için şunları açıkça **kapsam dışı** bırakıyor:
*"one-off project instructions, file paths, repo conventions, temporary workflow
details. Those belong in `AGENTS.md`, not `SOUL.md`."*

| | `AGENTS.md` (bu kol) | `SOUL.md` ([`../hermes/`](../hermes/)) |
|---|---|---|
| Kapsam | **Proje** — repo ile yaşar | **Ajan** — her yere seninle gider |
| İçerik | Komut, path, dokunma yasağı, iş akışı | Ses, ton, kararsızlıkta/itirazda davranış |
| Nerede durur | Proje kökü | `~/.hermes/profiles/<ad>/SOUL.md` |
| Değişme sıklığı | Proje değişince | Nadiren |

**Kısaca:** Hermes kullanıcısı `SOUL.md` **ve** `AGENTS.md` yazar. Proje kuralını
`SOUL.md`'ye koymak onu tüm projelere bulaştırır.

## İşe yaradı mı

İlk hafta şu üçünü say:

1. Ajan kapalı test dizinine kaç kez dokunmaya çalıştı → 0 olmalı
2. Kaç kez "bitti" dedi ama bitmemişti → düşmeli
3. İki ajan kaç kez aynı dosyada çakıştı → sahiplik bölümü çalışıyor mu

Bu üçü iyiyse şablon işini yapıyor. Değilse **eksik olan maddeyi** ekle —
dosyayı büyütmek değil, doğru maddeyi bulmak önemli.
