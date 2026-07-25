# Profil — Unity

> `docs/`'taki kurallara eşleme. Çelişki halinde `docs/` kazanır.

---

## 1. En kritik iki kalem

Unity'de iki şey diğer her şeyden önce gelir:

| # | Kalem | Neden |
|---|---|---|
| 1 | **Sahne/prefab çakışma politikası** | Unity'nin **multi-agent katili**. Sahne dosyası pratikte merge edilemez. Bu kurulmadan iki ajan aynı projede çalışamaz. |
| 2 | **Deterministik replay testi** | En yüksek ROI'li sadakat testi. Fizik regresyonunu tek hash karşılaştırmasıyla yakalar. |

---

## 2. Sahne ve prefab çakışması (docs/03 §6)

### 2.1 Zorunlu kurulum

```
1. Edit > Project Settings > Editor > Asset Serialization = Force Text
   (Binary kalırsa hiç merge edilemez — pazarlıksız ilk adım)

2. UnityYAMLMerge merge driver olarak kurulu
   git config merge.unityyamlmerge.name "Unity SmartMerge"
   git config merge.unityyamlmerge.driver \
     '"<Unity>/Contents/Tools/UnityYAMLMerge" merge -p %O %A %B %A'

3. .gitattributes → templates/gitattributes.example Unity bölümü

4. Git LFS: .psd .fbx .wav .mp4
```

### 2.2 Çalışma kuralları

| Kural | Detay |
|---|---|
| **Sahne = exclusive lease** | Aynı `.unity` dosyasına **iki açık PR YASAK**. Claim protokolünde exclusive olarak işaretlenir (`docs/03` §4). |
| **Feature = kendi prefab'ı** | Ajan sahneye doğrudan nesne eklemez; kendi prefab'ını yazar. |
| **Kompozisyonu tek integrator ajan yapar** | Prefab'ları sahneye bağlayan tek bir `agent:unity-integrator`. |
| **Prefab variant kullan** | Paylaşılan prefab'ı değiştirmek yerine variant türet. |
| **`.meta` daima asset'iyle aynı commit'te** | GUID kaybı tüm referansları kırar. |
| **Feature PR'ında asset taşıma/rename YASAK** | Ayrı PR, tek sahip. |
| **Asmdef = doğal fitness function** | Assembly definition referans kısıtları Unity'de mimari kuralı *derleyici seviyesinde* uygular. Kullan — `docs/04` §2'nin en ucuz uygulaması. |

> ⚠ **SmartMerge bile semantik çakışmayı çözmez.** Textual merge başarılı olsa da
> iki ajanın sahne değişikliği anlamsal olarak çakışabilir. Asıl kontrol exclusive lease'dir.

---

## 3. Test katmanı eşlemesi

| `docs/02` §3 katmanı | Unity karşılığı | Not |
|---|---|---|
| Unit (#12) | **EditMode** test | Saf mantık: durum makinesi, kural motoru, hesaplama. I/O'suz deterministik mantık **%100 EditMode ile test edilebilir** — en ucuz kazanç. |
| Property-based (#8) | EditMode + `FsCheck`/custom generator | Invariantlar: "skor negatif olamaz", "deste 52 kart korunur", "tur sırası döngüsel" |
| Integration (#5) | **PlayMode** test | Sahne/lifecycle/prefab entegrasyonu |
| Replay (#11) | **Deterministik replay** — §4 | Fizik/simülasyon içeren projelerde pilotla ölçülür |
| E2E (#10) | PlayMode uçtan uca senaryo | Max 10 |
| Perf (#13) | Profiler marker + CI eşiği | Frame bütçesi ihmal edilirse geri dönüşü pahalı |
| Architecture fitness (#4) | **asmdef referans kısıtları** + `NetArchTest` | §2.2 |
| Acceptance (#1) | PlayMode, `AC-###` etiketli | QA ajanı yazar |
| Golden (#11) | Sınırlı — render farkları gürültülü | Sadece UI, sahne değil |
| **Kullanım hissi** | ❌ **Test yazma** | `docs/05` §3.2 G5: bilinçli insan alanı. Kontrol tepkisi ve etkileşim hissi hiçbir assert ile ölçülemez. |

---

## 4. Deterministik replay testi

Fizik/simülasyon regresyonunu düşük maliyetle yakalayabilen bir mekanizma.

```
Kurulum:
  - Sabit seed          → Random.InitState(seed)
  - Sabit timestep      → Time.fixedDeltaTime sabit, Update yerine FixedUpdate
  - Kayıtlı input dizisi → frame -> input map, dosyadan
  - Çıktı               → final state hash (pozisyon/hız/skor, yuvarlanmış)

Test:
  replay(seed=42, inputs="fixtures/shot_001.json") == "a3f9c1..."
```

Zorunlu disiplin — bunlar olmadan replay flake üretir:
- Fizik/oyun mantığında `Time.deltaTime` **kullanma** (FixedUpdate + fixedDeltaTime)
- Fizik mantığında `Random` **kullanma** (yalnız seed'li generator)
- Float karşılaştırmasında hash öncesi **yuvarla** (platform farkı)
- Platform bazlı baseline tut (macOS/Linux fizik sonucu birebir aynı olmayabilir)

**Ne yakalar:** fizik parametresi kaymaları, çarpışma mantığı regresyonu ve hesap
zinciri bozulmaları. Hash yalnız kaydedilmiş oracle'a uyumu gösterir; oracle
yanlış, eksik veya ajan tarafından güncellenebilir durumdaysa doğru davranışı
kanıtlamaz. Fixture/baseline sahipliği QA'da kalır ve semantik invariant
testleriyle desteklenir.

---

## 5. Yüksek çekişmeli dosyalar (Unity'ye özgü)

| Dosya | Politika |
|---|---|
| `*.unity` | Exclusive lease · integrator ajan · §2.2 |
| `*.prefab` (paylaşılan) | Exclusive lease · variant tercih et |
| `*.meta` | Asset'iyle aynı commit · asla elle üretme/silme |
| `ProjectSettings/*.asset` | Tek sahip: `agent:techlead` |
| `Packages/manifest.json` | Tek sahip: `agent:deps` |
| `*.asmdef` | Tek sahip: `agent:techlead` (mimari kural taşır) |
| `*.controller`, `*.anim` | Exclusive lease (animator state machine merge edilemez) |

---

## 6. Fast lane (docs/06 §1)

Unity'de derleme yavaştır — fast lane hedefi zorlaşır. Stratejiler:

| Strateji | Kazanç |
|---|---|
| Library klasörünü CI'da cache'le | En büyük kazanç |
| Fast lane'de yalnız **EditMode** koş | PlayMode merge lane'e |
| Asmdef ile derlemeyi parçala | Kısmi yeniden derleme |
| `-batchmode -nographics` | Headless |
| PlayMode + replay testleri merge lane'de | Fast lane'i repo SLO'sunda tut |

Unity fast lane SLO'su ilk pilotta EditMode derleme/test p95'inden türetilir;
diğer stack'lerin eşiği doğrudan taşınmaz.

---

## 7. Unity'ye özgü anti-pattern'ler

| ❌ | Neden |
|---|---|
| İki ajanı aynı sahnede çalıştırmak | Merge pratikte imkânsız |
| Binary serialization ile git | Hiç merge edilemez |
| Fizik mantığında `Time.deltaTime` | Replay determinizmi ölür |
| Fizik mantığında seed'siz `Random` | Aynı |
| Feature PR'ında asset taşımak | GUID/referans kırılması |
| `.meta` dosyasını ayrı commit'lemek | Referans kaybı |
| Kural motorunu PlayMode'da test etmek | EditMode'da 100× hızlı test edilebilir |
| Kullanım hissi için otomatik test yazmaya çalışmak | Ölçülemez; G5 insan alanı |
| Sahne seviyesinde screenshot golden | Render farkı gürültüsü |
