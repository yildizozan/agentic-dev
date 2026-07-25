# Spec Değişim PR Şablonu

> Kullanım: `docs/06-operations.md` §4. Bir AC değiştiğinde bu şablonla PR açılır.
>
> **Neden şablon:** Multi-agent'ta spec değişimi bir **yarış durumudur**. Ajan A,
> AC-042 v1'e göre kod yazarken PM AC-042'yi v2'ye taşırsa A'nın işi sessizce
> geçersizleşir. Bu şablonun 4. ve 5. bölümü tam olarak onu engellemek için var.

---

## 1. Değişen AC

| | |
|---|---|
| AC ID | `AC-###` |
| Eski versiyon | v_ |
| Yeni versiyon | v_ |
| Tetikleyici | ☐ ürün kararı ☐ spec eksik/hatalı bulundu ☐ teknik kısıt ☐ gizli test tahkimi |

## 2. Delta — açıkça

**Önce:**
> <eski kabul davranışı, aynen>

**Sonra:**
> <yeni kabul davranışı, aynen>

**Değişmeyen:** <kapsam dışı kalanlar — ajanın gereksiz iş yapmasını engeller>

## 3. İnsan onayı (G4) — ZORUNLU

- [ ] Onaylayan: `<insan>`
- [ ] Tarih: `<YYYY-MM-DD>`

Ajan bu bölümü doldurmaz (`docs/05-roles.md` §3.2).

## 4. Etki analizi — ZORUNLU

### 4.1 Bu AC'yi referans veren testler
```
<kriter kapsaması kontrolü çıktısı veya: grep -rl "AC-###" tests/>
```

### 4.2 O testlerin kapsadığı kod
```
<impact analizi çıktısı — docs/04 §5>
```

### 4.3 Etkilenen path'lerde AÇIK CLAIM var mı?
```
<tasks/active/ veya issue tracker sorgusu — docs/03 §4>
```

| Açık claim | Ajan | Branch | Bildirim gönderildi mi |
|---|---|---|---|
| | | | ☐ |

## 5. Invalidation bildirimi — ZORUNLU

- [ ] Etkilenen tüm açık claim sahiplerine bildirim gönderildi
- [ ] Ajanlar **durdu** ve yeni AC'yi okudu
- [ ] Yeniden değerlendirme sonucu kaydedildi: ☐ devam ☐ yeniden başla ☐ iptal

> **Kural (`docs/03` §4.3):** "Devam edip sonra uydururuz" YASAK.
> Bildirim yoksa ajan eski gerçeklikte çalışmaya devam eder — multi-agent'taki
> en pahalı sessiz hata sınıfı budur.

## 6. Uygulama sırası

- [ ] 1. AC dosyası v(n+1) olarak güncellendi; eski versiyon `status: superseded` (**silinmedi**)
- [ ] 2. QA ajanı acceptance testini güncelledi — **ayrı PR** (`docs/02` §4.9)
- [ ] 3. Gizli set varyantı güncellendi + manifest kontrol edildi
- [ ] 4. Engineer implement etti — **ayrı PR**
- [ ] 5. Eski versiyonun testi silindi
- [ ] 6. Kriter kapsaması kontrolü yeşil (yeni versiyon testli, öksüz referans yok)

## 7. Geri alma planı

<Bu değişiklik yanlışsa nasıl geri alınır. Migration varsa özellikle.>
