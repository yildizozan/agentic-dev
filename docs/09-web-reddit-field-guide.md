# 09 — Web + Reddit Saha Rehberi

> **Tanımlayıcı ve operasyonel rehber.** Son tarama: **2026-07-25**.
> Bu repo bir runtime policy motoru değildir. Bu dosya, dış bulgudan rehber
> önerisine giden izi ve önerinin sınırlarını tutar.

## 1. Kanıtı nasıl okuyacağız?

Üç kaynak sınıfı birbirinin yerine geçmez:

| Sınıf | Ne için kullanılır | Ne için kullanılmaz |
|---|---|---|
| **A — Resmi/primary** | Ürün davranışı, güvenlik sınırı, araç semantiği | Başka bir organizasyonda beklenen etki büyüklüğünü garanti etmek |
| **B — Ampirik araştırma** | Belirli model/görev/örneklemde ölçülen etki | Sonucu bağlam belirtmeden evrensel eşik yapmak |
| **C — Reddit saha sinyali** | Tekrarlanan sorun hipotezi, yeni arama sorusu, ergonomi riski | Prevalans, nedensellik veya `MUST` kuralı |

Bir Reddit gönderisi ne kadar görünür olursa olsun anekdottur. Kullanıcılar
kendi seçilir, başarısızlıklar daha çok yazılır, ürün subreddit'lerinde pazarlama
ve astroturfing olabilir, gönderiler sonradan değişebilir veya silinebilir.

## 2. Bulgular → repo kararları

| Bulgu | Kanıt | Bu repodaki karar | Rehber sınıfı |
|---|---|---|---|
| `CODEOWNERS` sorumluyu ve review isteğini tanımlar; tek başına yazma kilidi değildir | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | Governance owner ile aktif write lease ayrıldı; gerçek enforcement hedef-repo ruleset/CI'ına bırakıldı | hedef-repo uyarlaması |
| Merge queue required check'leri `merge_group` olayında ayrıca koşmalıdır | [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [merge queue](https://docs.github.com/en/enterprise-cloud%40latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) | Opsiyonel pipeline örneği hem `pull_request` hem `merge_group` olayını gösterir; rehber reposunda self-CI kurulmaz | resmi semantik + örnek |
| PR kontrollü kodla secret aynı runner/job güven sınırında buluşmamalıdır | [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use), [pull_request_target güvenliği](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target), [compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners) | Hidden token/test clone örneği kaldırıldı; harici black-box evaluator yoksa hidden değerlendirme yalnız tasarım önerisidir | güvenlik önerisi |
| Üçüncü taraf Actions referansını tam commit SHA'ya sabitlemek değişmez kullanım sağlar | [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Opsiyonel pipeline örneği tam SHA, `contents: read` ve kapalı credential persistence gösterir | resmi semantik + örnek |
| Lockfile politikası ekosisteme ve paket türüne bağlıdır; uygulama lockfile'ları reproducibility için source control'e alınır | [npm package-lock](https://docs.npmjs.com/cli/v6/configuring-npm/package-lock-json/), [Dart `pub get`](https://dart.dev/tools/pub/cmd/pub-get), [Dart private files](https://dart.dev/tools/pub/private-files) | Normatif metin ve stack profilleri düzeltildi; korumalı `templates/ownership-map.yml` için Tech Lead + insan güncellemesi açık geçiş işi olarak bırakıldı | stack'e özgü öneri |
| `union`/`ours` bir metin birleşim tercihi yapar; domain semantiğini doğrulamaz | [Git merge-file](https://git-scm.com/docs/git-merge-file), [gitattributes](https://git-scm.com/docs/gitattributes) | Lockfile, i18n, registry ve route tablolarında otomatik `union/ours` kaldırıldı; parser/invariant kontrolü önerildi | semantik güvenlik önerisi |
| Worktree birden çok branch'i ayrı working tree'lerde açar; bu dosya izolasyonudur | [Git worktree](https://git-scm.com/docs/git-worktree) | Hedef repoda her ajan için ayrı worktree önerilir; aynı path lease'i ve birleşik-state doğrulaması ayrıca gerekir | operasyon önerisi |
| Impact graph'ı belirli SWE-bench/model düzeninde regresyonu düşürdü | [TDAD arXiv 2603.17973](https://arxiv.org/abs/2603.17973) | Impact analysis tutuldu; `%70` evrensel vaat veya gate eşiği olmaktan çıkarıldı | hipotez + lokal baseline |
| Operasyonel ajan hataları yalnız test/derleme kırığı değildir | [What Breaks When LLMs Code?](https://arxiv.org/abs/2605.30777) | Yetki sınırı, destructive-action disiplini ve ajan raporu ≠ dış kanıt ayrımı korundu | ampirik risk modeli |
| Hidden split ve semantic mutation, tool-using agent prompt derleme domain'inde ölçüldü | [TDAD Agent Definition](https://arxiv.org/abs/2603.08806) | Kod ajanlarına doğrudan transfer edilmedi; hidden evaluator ve eşikler hedef repoda ölçülene kadar pilot fikridir | analog kanıt |

## 3. Reddit saha sinyalleri

Bu bölüm “ne kadar sık oluyor?” sorusunu yanıtlamaz. “Hangi failure mode için
ölçüm veya guardrail tasarlamalıyız?” sorusuna aday üretir.

### 3.1 Testi değiştirerek yeşile dönme

[r/ClaudeAI'daki bir kullanıcı](https://www.reddit.com/r/ClaudeAI/comments/1k30oip/i_stopped_using_37_because_it_cannot_be_trusted/)
ajanın kırılan üretim davranışını düzeltmek yerine testleri zayıflattığını veya
sildiğini raporluyor. Aynı gönderide salt prompt yasağının bunu her zaman
engellemediği anlatılıyor.

**Yorum:** Tek gönderi prevalans kanıtı değildir; fakat “kod ajanı kritik oracle'yı
yazabilir mi?” tehdidi için somut adversarial senaryodur.

**Hedef-repo karşılığı:** Mevcut acceptance/regression oracle'ları, görünür hidden
manifest ve contract'lar Engineer path'inden ayrıdır; gerçek hidden oracle harici
evaluator'dadır. Yeni acceptance oracle'ı QA-imzalı, path-pure commit olur.
Red proof adapter'ı beklenen test kimliği ve assertion sınıfını doğrulamıyorsa
mekanizma yalnız pilot önerisidir.

### 3.2 Review hızı, üretim hızına yetişmeyebilir

[AI-üretimi kodun review yükü tartışması](https://www.reddit.com/r/cursor/comments/1so1xzn/how_are_you_handling_code_review_when_most_of_the/)
ve [teknik borç tartışması](https://www.reddit.com/r/cursor/comments/1p210g4/how_are_you_guys_dealing_with_tech_debt/)
hızlı üretimin review süresini, ölü kodu ve bakım belirsizliğini artırabildiğine
dair saha örnekleri sunuyor.

**Yorum:** Bu paylaşımlar kontrollü deney değildir. Yine de yalnız “PR sayısı” veya
“üretilen LOC” ölçmenin ters teşvik yaratacağı hipotezini güçlendirir.

**Hedef-repo karşılığı:** İnsan review dakikası / merge edilmiş AC, çöpe giden iş,
revert ve ölü kod trendi gözlemsel metrik olarak tutulur. Riskli path'ler G2'ye
gider; her diff'e aynı review bütçesi verilmez.

### 3.3 Worktree dosyayı ayırır, ortamı değil

Toplulukta [aynı repo için birden çok ajan](https://www.reddit.com/r/ClaudeCode/comments/1sr2ni6/how_are_you_guys_managing_multiple_ai_coding/),
[worktree kullanımı](https://www.reddit.com/r/codex/comments/1s4wns4/how_do_you_deal_with_multiple_agents_in_the_same/)
ve [eksik `.env`/virtualenv kaynaklı kırık worktree ortamı](https://www.reddit.com/r/codex/comments/1rt8m3w/how_are_you_handling_broken_environments_when/)
ayrı ayrı tartışılıyor.

**Yorum:** Resmi Git dokümanı yalnız working-tree semantiğini garanti eder.
Secret paylaşımı, port çakışması, DB state'i, cache ve runtime izolasyonu ayrı
tasarım problemidir. Reddit burada çözüm kanıtından çok ergonomi/operasyon
backlog'u üretir.

**Hedef-repo karşılığı:** “worktree var → izolasyon tamam” denmez. Hedef repo, her
worktree için environment manifesti, benzersiz port/namespace ve secret
provisioning sınırını ayrıca tanımlar. Secret kopyalamak varsayılan çözüm değildir.

### 3.4 “Bitti” raporu objektif stop signal olmayabilir

[Tamamlanmamış işin tamamlandı raporlanması tartışması](https://www.reddit.com/r/ClaudeCode/comments/1rwd8fa/why_ai_coding_agents_say_done_when_the_task_is/)
geniş ve belirsiz görevlerde objektif durma sinyali eksikliğine dikkat çekiyor.
Bu saha sinyali, ampirik güvenlik çalışmasındaki fabricated-success kategorisiyle
aynı risk ailesine işaret ediyor; ikisi aynı kanıt türü değildir.

**Hedef-repo karşılığı:** “Ajan geçti dedi” gate değildir. Lokal sonuç kanıttır ama
merge tamamlanması için uzak required CI yeşili gerekir. Kapsamı belirsiz görev,
ölçülebilir AC olmadan başlamaz.

## 4. Bu repoda günlük çalışma akışı

### 4.1 Yazmadan önce

1. Soruyu tek cümleyle yaz: “Hangi iddia veya failure mode hakkında karar
   veriyorum?”
2. En az bir resmi/primary web kaynağı ara. Ürün semantiği için vendor dokümanı,
   ölçüm için paper/dataset/repo tercih et.
3. Aynı failure mode için Reddit ara. Çözüm kopyalamak için değil; saha
   varyantlarını ve ergonomi sorunlarını bulmak için.
4. Bu dosyaya tarih, sorgu, kaynak sınıfı, bulgu ve repo etkisini ekle.
5. İlgili yerel Markdown bölümlerini ve mevcut kaynak kayıtlarını oku; dış
   kaynak bu rehberin iç tutarlılığını açıklamaz.
6. Etkilenen rehber bölümleri kesinleşince dar kapsamlı düzenleme yap.

### 4.2 Yazarken

- Bir dış öneriyi doğrudan evrensel ve zorunlu kural ilan etme.
- Resmi doküman araç davranışını doğrulasa bile hedef repodaki branch protection,
  secret policy veya CI sonucunu var sayma.
- Reddit'te tekrarlanan bir sorun için önce hedef-repo pilotu veya gözlemsel
  metrik tasarla.
- Eşik gerekiyorsa ilk baseline'ı, örneklem penceresini ve hata maliyetini yaz.

### 4.3 PR/merge öncesi

- Kaynak linkleri doğrudan destekledikleri cümlenin yanında mı?
- Reddit bulgusu açıkça “anekdot/saha sinyali” diye etiketli mi?
- Paper sonucu model, benchmark, örneklem ve tarih bağlamıyla mı yazıldı?
- Otomatik uygulanıyor denen bir önerinin hedef-repo kanıtı gerçekten var mı?
- CI örneği değiştiyse PR ve `merge_group` aynı required kontrolü gösteriyor mu?
- Güvenlik örneği PR kontrollü kodu secret/hidden oracle ile aynı trust
  boundary'ye koyuyor mu?

## 5. Araştırma kayıt şablonu

Yeni tarama bu biçimde eklenir:

```markdown
### YYYY-MM-DD — <karar sorusu>

- Resmi/primary sorgu: `<arama sorgusu>`
- Reddit sorgu: `<arama sorgusu>`
- Resmi bulgu: <araç semantiği veya ölçüm; doğrudan link>
- Reddit sinyali: <anekdot; doğrudan thread linkleri>
- Çelişen/negatif bulgu: <varsa>
- Repo etkisi: <rehber bölümü veya örnek dosya>
- Karar: adopt | pilot | reject | no-change
- Güven: high | medium | low
```

## 6. 2026-07-25 sorgu kaydı

Resmi/primary web sorguları:

- `GitHub CODEOWNERS write restriction required review`
- `GitHub Actions merge queue merge_group checks_requested`
- `GitHub Actions secure use pin full commit SHA untrusted pull request`
- `npm package-lock commit source control`
- `Dart pubspec.lock application check source control`
- `git worktree multiple working trees`
- `arXiv 2603.17973`, `2603.08806`, `2605.30777`

Reddit sorguları:

- `AI coding agent deleted tests changed tests to pass`
- `AI generated code review overhead technical debt`
- `multiple coding agents git worktree conflicts`
- `worktree broken environment env virtualenv ports`
- `coding agent says done incomplete task`

## 7. Açık araştırma soruları

- Hedef repolarda agent-written test tampering oranı nedir? Tekil olay değil,
  paydalı ölçüm gerekiyor.
- Worktree başına runtime/port/DB izolasyonunun maliyeti ve çakışma azalması nedir?
- Per-test collector adapter'ı hangi framework'lerde güvenilir test kimliği ve
  assertion failure sınıfı üretebilir?
- Harici hidden evaluator, oracle sızdırmadan yeterli debug sinyalini nasıl verir?
- Risk-sıralı review gerçekten insan dakikası / AC metriğini düşürüyor mu?
- Korumalı `templates/ownership-map.yml`, sahibi tarafından §1 ownership/lease
  ayrımı ve §6 lockfile politikasıyla ne zaman uzlaştırılacak?

Bu sorular cevaplanmadan ilgili maddeler hedef-repo önerisi veya açık araştırma
sorusu olarak kalır; doküman dili onları kendiliğinden uygulanmış kontrol yapmaz.
