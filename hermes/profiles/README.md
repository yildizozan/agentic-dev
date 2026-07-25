# hermes/profiles/ — kullanıma hazır profiller

Her dizin bir Hermes profiline karşılık gelir ve içinde **doldurulmuş, hazır bir
`SOUL.md`** vardır. Placeholder yok — kopyala ve kullan.

Sıfırdan yazmak istersen: [`../SOUL.template.md`](../SOUL.template.md)

| Profil | Rolü | Ne zaman |
|---|---|---|
| [`dev/`](dev/SOUL.md) | İnşa eden | Ana geliştirme. Buradan başla. |
| [`qa/`](qa/SOUL.md) | Doğrulayan | Kabul testi/kontrol üretimi |
| [`review/`](review/SOUL.md) | İnceleyen | Değişiklik incelemesi |
| [`research/`](research/SOUL.md) | Araştıran | Karar öncesi kaynak taraması |

---

## Kurulum

```bash
# tek profil
hermes profile create dev
cp hermes/profiles/dev/SOUL.md ~/.hermes/profiles/dev/SOUL.md
dev chat

# dördü birden
for p in dev qa review research; do
  hermes profile create "$p"
  cp "hermes/profiles/$p/SOUL.md" "$HOME/.hermes/profiles/$p/SOUL.md"
done
hermes profile list
```

Her profil `~/.hermes/profiles/<ad>/` altında kendi `config.yaml`, `.env`,
`SOUL.md`, skill ve memory'siyle **izoledir**. Alias otomatik: `~/.local/bin/<ad>`.

---

## Neden ayrı profil — üç somut sebep

| Sebep | Açıklama |
|---|---|
| **Kendi sınavını yazan ajan hizalanmış değildir** | Kodu yazan ajan geçeceği kabul testini yazmamalı. `dev` ve `qa` ayrı profil = ayrı context. |
| **Korelasyonlu hata** | Aynı modelin kendi kodunu review etmesi aynı kör noktayı iki kez kaçırır. `review` için **farklı model** ata (`config.yaml`). |
| **Rol karışması** | Tek profile hem "inşa et" hem "şüpheci ol" demek ikisini de zayıflatır. |

Farklı model ataması profil bazlı yapılır:

```bash
$EDITOR ~/.hermes/profiles/review/config.yaml   # model/provider'ı dev'den farklı seç
```

---

## Bunlar proje kuralı içermez

Dördünün hiçbirinde komut, path, port veya dizin yasağı yok — olmaması gerekiyor.
`SOUL.md` her projeye seninle gider; proje kuralı oraya girerse yanlış projede
yanlış kural uygular.

Proje tarafı: [`../../harness/AGENTS.template.md`](../../harness/AGENTS.template.md)

| Bu dosyalarda ne var | Nerede olmalı |
|---|---|
| Ses, ton, doğrudanlık | ✅ burada (`SOUL.md`) |
| Kararsızlık/itiraz davranışı | ✅ burada |
| Kanıt ve tamamlanma disiplini | ✅ burada |
| `npm test`, `tests/` yasakları, port | ❌ `AGENTS.md` |

---

## Uyarlama

Dosyalar olduğu gibi çalışır ama seninkiler olmalı:

1. **İlk satırdaki adı** değiştir (`Sen dev.` → kendi adlandırman).
2. **Çalıştığın ortam** satırını kendine göre yaz — ton kalibrasyonunu o belirler.
3. İhtiyacın olmayan bölümü **sil**. `SOUL.md` her istekte yükleniyor; şişkin
   dosya hem para yakar hem talimatları seyreltir.

Hedef 40 satır civarı. Bir bölüm işe yaramıyorsa **keskinleştir**, yeni bölüm
ekleyerek dosyayı büyütme.
