# hermes/ — profile `SOUL.md` yazacaksan buradasın

[Hermes Agent](https://hermes-agent.nousresearch.com/) (NousResearch) için.
Bu kol **ajan kapsamlı** kimliği üretir: ajanın kim olduğu, nasıl konuştuğu,
kararsızlıkta ve itirazda ne yaptığı.

---

## 👉 Tek adım

**Hazır profiller** → [`profiles/`](profiles/) — dördü de doldurulmuş, placeholder yok:

```bash
for p in dev qa review research; do
  hermes profile create "$p"
  cp "hermes/profiles/$p/SOUL.md" "$HOME/.hermes/profiles/$p/SOUL.md"
done
dev chat
```

| Profil | Rolü |
|---|---|
| [`profiles/dev/SOUL.md`](profiles/dev/SOUL.md) | İnşa eden — **buradan başla** |
| [`profiles/qa/SOUL.md`](profiles/qa/SOUL.md) | Doğrulayan |
| [`profiles/review/SOUL.md`](profiles/review/SOUL.md) | İnceleyen |
| [`profiles/research/SOUL.md`](profiles/research/SOUL.md) | Araştıran |

Sıfırdan yazacaksan: **[`SOUL.template.md`](SOUL.template.md)**

`SOUL.md` system prompt'un **1. slotuna**, sarmalayıcı metin eklenmeden girer —
yani ajanın ilk okuduğu şeydir.

---

## Önce şunu bil: `SOUL.md` operasyonel kural dosyası DEĞİL

En sık yapılan hata proje kurallarını `SOUL.md`'ye doldurmak. Resmi kural:

> *"if it should follow you everywhere, it belongs in `SOUL.md`;
> if it belongs to a project, it belongs in `AGENTS.md`"*
> — [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)

Aynı doküman `SOUL.md` için şunları **açıkça kapsam dışı** bırakıyor:
*"one-off project instructions, file paths, repo conventions, temporary workflow
details. Those belong in `AGENTS.md`, not `SOUL.md`."*

| | `SOUL.md` (bu kol) | `AGENTS.md` ([`../harness/`](../harness/)) |
|---|---|---|
| Kapsam | **Ajan** — her projeye seninle gider | **Proje** — repo ile yaşar |
| İçerik | Ses, ton, doğrudanlık, kararsızlık/itiraz davranışı | Komut, path, dokunma yasağı, iş akışı |
| Yeri | `~/.hermes/profiles/<ad>/SOUL.md` | Proje kökü |
| Değişme sıklığı | Nadiren | Proje değişince |

> **Hermes ikisini birlikte okur.** Yazılım geliştiren bir profil için
> **ikisi de gerekli**: kimlik burada, proje kuralları
> [`../harness/AGENTS.template.md`](../harness/AGENTS.template.md)'de.
>
> Proje kuralını `SOUL.md`'ye koyarsan onu **tüm projelere** bulaştırırsın —
> ve `SOUL.md` her yere gittiği için yanlış projede yanlış kural uygular.

---

## Profil yapısı

Her profil ayrı bir Hermes home dizini; kendi `config.yaml`, `.env`, `SOUL.md`,
memory, session, skill ve cron'una sahip ve diğerlerinden **izole**.

```
~/.hermes/profiles/<ad>/
  config.yaml      model, provider, toolset
  .env             API key / token
  SOUL.md          ← bu kolun ürettiği dosya
  skills/          öğrenilen + kurulan skill'ler
  memories/  sessions/  state db
```

Sık kullanılan komutlar:

| Komut | Ne yapar |
|---|---|
| `hermes profile create <ad>` | Boş profil (bundled skill'lerle) |
| `hermes profile create <ad> --clone` | `config.yaml`, `.env`, `SOUL.md`, skill'leri kopyalar |
| `hermes profile create <ad> --clone-from <kaynak>` | Belirli profilden klonlar |
| `hermes -p <ad> chat` · `<ad> chat` | Profili kullan (alias `~/.local/bin/<ad>`) |
| `hermes profile use <ad>` | Yapışkan varsayılan |
| `hermes profile list` · `rename` · `delete` | Yönetim |

**Not:** Hermes `SOUL.md`'yi yalnız `HERMES_HOME`'dan okur — çalışma dizininden
**okumaz**. Projeye `SOUL.md` koymak işe yaramaz; oraya `AGENTS.md` koyacaksın.

Kaynak: [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles/) ·
[Use SOUL.md with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes)

---

## Rol başına profil önerisi

Bu rehberin rol ayrımı ([`../docs/05-roles.md`](../docs/05-roles.md)) Hermes
profillerine doğrudan oturur. Kritik olan: **kodu yazan ajan, geçeceği kabul
testini yazmasın.** Ayrı profil = ayrı context = ayrı `SOUL.md`.

| Profil | `SOUL.md` eğilimi | Neden ayrı |
|---|---|---|
| [`dev`](profiles/dev/SOUL.md) | İnşa eden, kapsamı dar tutan | Ana iş |
| [`qa`](profiles/qa/SOUL.md) | Şüpheci, kabul kriterinden kontrol üreten | Kendi sınavını yazan ajan hizalanmış değildir |
| [`review`](profiles/review/SOUL.md) | Karşı çıkmaya eğilimli, **farklı model** | Aynı modelin kendi kodunu review etmesi korelasyonlu hata üretir |
| [`research`](profiles/research/SOUL.md) | Kaynağı görünür kılan | Kanıt sınıflarını karıştırmamak için |

Dördü de [`profiles/`](profiles/) altında hazır. `review` için `config.yaml`'da
`dev`'den **farklı model** ata — sebebi yukarıdaki satırda.

---

## `SOUL.md`'de ne var, ne yok

| ✅ `SOUL.md`'ye | ❌ `AGENTS.md`'ye |
|---|---|
| "Doğrudan ol, yağlama yapma" | "`npm test` koş" |
| "Emin değilsen tahmin etme, sor" | "`tests/acceptance/` dizinine dokunma" |
| "Bitmeyen işi bitmiş gösterme" | "`main`'e push etme" |
| "İtirazını bir kez söyle, sonra kararı uygula" | "port 5432 kullan" |
| "Belirsizliği adıyla söyle" | "migration'ı ayrı PR yap" |

Soldaki her satır **taşınabilir karakter**; sağdaki her satır **projeye ait olgu**.
Karar veremiyorsan sor: *"bu kural yarın başka bir projede de geçerli mi?"*
Evetse `SOUL.md`, hayırsa `AGENTS.md`.
