# hermes/profiles/ — kullanıma hazır rol profilleri

Her dizin bir Hermes profiline karşılık gelir ve içinde **doldurulmuş, hazır bir
`SOUL.md`** vardır. Placeholder yok — kopyala ve kullan.

Roller [`../../docs/05-roles.md`](../../docs/05-roles.md) §1'deki sorumluluk
matrisiyle hizalıdır.

| Profil | Rol | Sınırı (`SOUL.md`'de yazılı) |
|---|---|---|
| [`project-manager/`](project-manager/SOUL.md) | PM · Project Lead · Product Owner · Producer | Uygulamayı seçmez, test/kod yazmaz |
| [`tech-lead/`](tech-lead/SOUL.md) | Tech Lead | Kabul kriterinin sahibi değil; kendine istisna tanımaz |
| [`engineer-backend/`](engineer-backend/SOUL.md) | Backend | Şema/sözleşmeyi tek taraflı değiştirmez |
| [`engineer-frontend/`](engineer-frontend/SOUL.md) | Frontend | Tasarım sabitini kendi seçmez |
| [`engineer-mobile/`](engineer-mobile/SOUL.md) | Mobile | Cihaz gerçeğini istisna saymaz |
| [`engineer-ui-ux/`](engineer-ui-ux/SOUL.md) | UI/UX implementation | Tasarım kararını vermez |
| [`engineer-unity/`](engineer-unity/SOUL.md) | Unity / simülasyon | Paylaşılan sahneye tek başına dokunmaz |
| [`qa/`](qa/SOUL.md) | QA | Kriteri icat etmez, üretim kodu yazmaz |
| [`security/`](security/SOUL.md) | Security | Riski kabul kararını vermez, korku pazarlamaz |
| [`product-designer/`](product-designer/SOUL.md) | Product Designer | Kapsamı belirlemez, fonksiyonel test yazmaz |

Sıfırdan yazacaksan: [`../SOUL.template.md`](../SOUL.template.md)

---

## Kurulum

```bash
# tek profil
hermes profile create tech-lead
cp hermes/profiles/tech-lead/SOUL.md ~/.hermes/profiles/tech-lead/SOUL.md
tech-lead chat

# hepsi
for p in project-manager tech-lead engineer-backend engineer-frontend \
         engineer-mobile engineer-ui-ux engineer-unity qa security product-designer; do
  hermes profile create "$p"
  cp "hermes/profiles/$p/SOUL.md" "$HOME/.hermes/profiles/$p/SOUL.md"
done
hermes profile list
```

İhtiyacın olmayan profili hiç açma. Her profil ayrı `~/.hermes/profiles/<ad>/`
dizini, kendi `config.yaml`, `.env`, `SOUL.md`, skill ve memory'siyle **izoledir**.
Alias otomatik: `~/.local/bin/<ad>`.

---

## Neden ayrı profil — üç somut sebep

| Sebep | Açıklama |
|---|---|
| **Kendi sınavını yazan taraf hizalanmış değildir** | Kodu yazan ile kabul kontrolünü yazan aynı olmamalı. `engineer-*` ve `qa` ayrı profil = ayrı context. |
| **Korelasyonlu hata** | Aynı modelin kendi çıktısını incelemesi aynı kör noktayı iki kez kaçırır. `tech-lead` (inceleme sahibi) için **farklı model** ata. |
| **Rol karışması** | Tek profile hem "inşa et" hem "şüpheci ol" hem "kapsamı belirle" demek üçünü de zayıflatır. |

Farklı model ataması profil bazlı:

```bash
$EDITOR ~/.hermes/profiles/tech-lead/config.yaml   # engineer-* profillerinden farklı model
```

---

## Yeni disiplin eklemek

Listede olmayan bir mühendislik disiplini gerekiyorsa (veri, ML, gömülü, devops…):

1. En yakın `engineer-*` profilini kopyala.
2. Yalnız **`## Disiplinim`** bölümünü değiştir.
3. Geri kalan bölümler (ses, kanıt, kapsam, bütünlük, itiraz) aynı kalır —
   ortak mühendislik disiplinidir, disipline göre değişmez.

`## Disiplinim` bölümüne **teknik detay değil eğilim** yaz. Framework adı, komut,
dizin ve port oraya değil `AGENTS.md`'ye ait.

---

## Bunlar proje kuralı içermez

Hiçbirinde komut, path, port veya dizin yasağı yok — olmaması gerekiyor.
`SOUL.md` her projeye seninle gider; proje kuralı oraya girerse yanlış projede
yanlış kural uygular.

Proje tarafı: [`../../harness/AGENTS.template.md`](../../harness/AGENTS.template.md)

| Bu dosyalarda ne var | Nerede olmalı |
|---|---|
| Ses, ton, doğrudanlık | ✅ burada (`SOUL.md`) |
| Kararsızlık / itiraz davranışı | ✅ burada |
| Kanıt ve tamamlanma disiplini | ✅ burada |
| Rolün sınırı — neye karışmadığı | ✅ burada |
| `npm test`, `tests/` yasakları, port, framework | ❌ `AGENTS.md` |

---

## Uyarlama

Dosyalar olduğu gibi çalışır ama seninkiler olmalı:

1. **İlk satırdaki adı** kendi adlandırmanla değiştir.
2. **Muhatap** satırını kendine göre yaz — ton kalibrasyonunu o belirler.
3. İhtiyacın olmayan bölümü **sil**. `SOUL.md` her istekte yükleniyor; şişkin
   dosya hem maliyet yakar hem talimatları seyreltir.

Bir bölüm işe yaramıyorsa **keskinleştir**, yeni bölüm ekleyerek dosyayı büyütme.

## İşe yaradı mı

İlk hafta profil başına şunu izle:

1. "Bitti" deyip bitirmediği durum sayısı → düşmeli
2. Emin olmadığında tahmin yerine sorduğu durum sayısı → artmalı
3. Rol sınırını aştığı durum sayısı (PM kod yazdı, QA implementasyon önerdi…) → düşmeli
