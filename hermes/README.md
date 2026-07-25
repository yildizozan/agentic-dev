# hermes/ — profile `SOUL.md` yazacaksan buradasın

[Hermes Agent](https://hermes-agent.nousresearch.com/) (NousResearch) için.
Bu kol **ajan kapsamlı** kimliği üretir: ajanın kim olduğu, nasıl konuştuğu,
kararsızlıkta ve itirazda ne yaptığı.

---

## 👉 Tek adım

**Hazır rol profilleri** → [`profiles/`](profiles/) — onu da doldurulmuş, placeholder yok:

| Profil | Rol |
|---|---|
| [`project-manager`](profiles/project-manager/SOUL.md) | PM · Project Lead · Product Owner · Producer |
| [`tech-lead`](profiles/tech-lead/SOUL.md) | Tech Lead |
| [`engineer-backend`](profiles/engineer-backend/SOUL.md) | Backend |
| [`engineer-frontend`](profiles/engineer-frontend/SOUL.md) | Frontend |
| [`engineer-mobile`](profiles/engineer-mobile/SOUL.md) | Mobile |
| [`engineer-ui-ux`](profiles/engineer-ui-ux/SOUL.md) | UI/UX implementation |
| [`engineer-unity`](profiles/engineer-unity/SOUL.md) | Unity / simülasyon |
| [`qa`](profiles/qa/SOUL.md) | QA |
| [`security`](profiles/security/SOUL.md) | Security |
| [`product-designer`](profiles/product-designer/SOUL.md) | Product Designer |

```bash
hermes profile create tech-lead
cp hermes/profiles/tech-lead/SOUL.md ~/.hermes/profiles/tech-lead/SOUL.md
tech-lead chat
```

Hepsini birden kurmak ve yeni disiplin eklemek: [`profiles/README.md`](profiles/README.md)
İhtiyacın olmayan profili hiç açma.

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

Rol ayrımı Hermes profillerine doğrudan oturur. Kritik olan: **kodu yazan ajan, geçeceği kabul
testini yazmasın.** Ayrı profil = ayrı context = ayrı `SOUL.md`.

| Profil | `SOUL.md` eğilimi | Neden ayrı |
|---|---|---|
| `project-manager` | Kapsamı ve kriteri tanımlayan | Kriteri yazan taraf onu doğrulamaz |
| `tech-lead` | Sözleşme kuran, adversarial inceleyen | **Farklı model** ata: aynı model kendi çıktısını incelerken aynı kör noktayı iki kez kaçırır |
| `engineer-*` | İnşa eden (disiplin başına) | Kendi geçeceği kabul kontrolünü yazmaz |
| `qa` | Şüpheci, kriterden kontrol üreten | Bağımsızlığı için üretim kodu yazmaz |
| `security` | Kırmızı çizgi bekçisi | Riski kabul kararını vermez |
| `product-designer` | Tasarım sözleşmesi sahibi | Fonksiyonel doğrulama yazmaz |

Onu da [`profiles/`](profiles/) altında hazır.

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
