# Agentic Development

Ajanlarla yazılım geliştirirken ajanlara **ne söyleyeceğini** veren iki şablon.

## Hangi dosyayı yazacaksın?

| | **[`harness/`](harness/)** | **[`hermes/`](hermes/)** |
|---|---|---|
| Ürettiğin dosya | **`AGENTS.md`** | **`SOUL.md`** |
| Kapsam | **Proje** — repo ile yaşar | **Ajan** — her yere seninle gider |
| İçerik | Komut, path, dokunma yasağı, iş akışı | Ses, ton, kararsızlık/itiraz davranışı |
| Nereye koyulur | Proje kökü | `~/.hermes/profiles/<ad>/SOUL.md` |
| Ortam | Claude Code · Codex · Cursor · Hermes | Hermes |
| Ne alırsın | **[`AGENTS.template.md`](harness/AGENTS.template.md)** — doldur | **[10 rol profili](hermes/profiles/)** — hazır, doldurulmuş |

İkisi de tek başına çalışır. Başka hiçbir dosyayı okumana gerek yok.

## Hermes kullanıyorsan ikisi de gerekli

"Hermes'te `SOUL.md` var, `AGENTS.md` gerekmez" yaygın bir yanlış — Hermes
**ikisini birlikte okur**:

> *"if it should follow you everywhere, it belongs in `SOUL.md`;
> if it belongs to a project, it belongs in `AGENTS.md`"*
> — [Hermes: Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)

Proje kuralını `SOUL.md`'ye koyarsan tüm projelere bulaşır.

## Roller

`hermes/profiles/` altında hazır: `project-manager` (PM · lead · owner · producer) ·
`tech-lead` · `engineer-backend` · `engineer-frontend` · `engineer-mobile` ·
`engineer-ui-ux` · `engineer-unity` · `qa` · `security` · `product-designer`

```bash
hermes profile create tech-lead
cp hermes/profiles/tech-lead/SOUL.md ~/.hermes/profiles/tech-lead/SOUL.md
tech-lead chat
```

---

`AGENTS.md` (bu repo kökünde) bu **rehbere** katkı yapan ajan içindir;
senin projendeki ajan için olan → [`harness/AGENTS.template.md`](harness/AGENTS.template.md)
