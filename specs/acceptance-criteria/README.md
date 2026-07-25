# Kabul Kriterleri (AC)

Spec'in yaşadığı yer. Kural: [`docs/02-spec-fidelity.md`](../../docs/02-spec-fidelity.md) §2

---

## Altın kural

> Her aktif `AC-###` için, **görünür test suite'inde veya gizli set manifest'inde**
> o ID'ye referans veren en az bir test bulunmak ZORUNLUDUR. Bulunmuyorsa build kırmızıdır.

Uygulayan: [`tools/criteria_coverage.py`](../../tools/criteria_coverage.py) — fast lane adımı.

## İnsan onayı zorunlu (G1)

`approved: true` + `approved_by` olmadan bir AC **aktif sayılmaz ve implementasyon başlamaz.**
Checker onaysız aktif AC'de build'i kırar.

Bu alanı **ajan doldurmaz.** Gerekçe: [`docs/05-roles.md`](../../docs/05-roles.md) §3.1 —
AC'yi LLM yazıp testi LLM üretip kodu LLM yazarsa döngü kendi içinde tutarlı biçimde
yanlış olabilir. AC onayı zincirdeki tek ground truth'tur.

## Yeni AC ekleme

```bash
cp templates/acceptance-criteria.md specs/acceptance-criteria/AC-0XX.md
# doldur → insan onaylar → QA ajanı çalıştırılabilir teste çevirir
python3 tools/criteria_coverage.py     # yeşil mi
```

Yazar sırası: PM ajanı taslak → **insan onay** → QA ajanı otomasyon
([`docs/05`](../../docs/05-roles.md) §2).

## Değiştirme

AC dosyası **hiç silinmez.** Değişimde `status: superseded` olur ve yeni versiyon açılır —
testler ID referansı taşıdığı için silinen AC öksüz test üretir.

Protokol: [`docs/06-operations.md`](../../docs/06-operations.md) §4 ·
Şablon: [`templates/spec-change.md`](../../templates/spec-change.md)

> ⚠ Açık claim'i olan bir AC sessizce değiştirilemez — invalidation bildirimi zorunludur.
> Aksi halde ajan eski gerçeklikte çalışmaya devam eder.

## Etiketleme konvansiyonu

| Durum | Nasıl |
|---|---|
| Normal test | AC ID doğrudan test adında/gövdesinde geçer |
| Fixture ID üreten meta-test | Dosyaya `criteria-coverage:ignore-file` işareti + yanına `.tags` beyan dosyası |
| Gizli test | AC ID `tests/hidden/manifest.txt`'e yazılır (içerik yazılmaz) |

**Tuzak:** Taranan bir dosyanın *yorumunda* bile var olmayan bir AC ID'si geçerse öksüz
referans olarak raporlanır. Örnek/fixture ID'lerini taranan dosyalara yazma.

## Mevcut AC'ler

| ID | Başlık | Onay | Gizli |
|---|---|---|---|
| [AC-001](AC-001.md) | Repo kurallarının çalıştırılabilir olduğu doğrulanır | ✅ | ❌ |
