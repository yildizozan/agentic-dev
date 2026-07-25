# Profil — Flutter

> `docs/`'taki kurallara eşleme. Çelişki halinde `docs/` kazanır.

---

## 1. Test katmanı eşlemesi

Sıra önemli: **Unit → Widget → `integration_test` → golden.**

| `docs/02` §3 katmanı | Flutter karşılığı | Not |
|---|---|---|
| Unit (#12) | `test/` saf Dart | Domain mantığı, mapper, validator |
| Property-based (#8) | `glados` / custom generator | Para, kota, form validasyonu, state machine |
| Integration/component (#5) | **Widget test** (`testWidgets`) | Gerçek widget ağacı. Flutter'da "trophy gövdesi" burasıdır. |
| Contract (#2) | OpenAPI'den üretilmiş client + şema doğrulama | Backend ajanıyla desync'in patladığı yer |
| Statik (#3) | `analysis_options.yaml` strict + `dart analyze` + `dart_code_metrics` | |
| Architecture fitness (#4) | `dart_code_metrics` banned imports + custom lint | §3 |
| E2E (#10) | `integration_test` gerçek cihaz/emülatör | Max 10 yolculuk |
| Golden (#11) | `matchesGoldenFile` | ⚠ §4 — kısıtlı kullanım |
| Visual/token (#14) | **Design token diff** | Screenshot diff'ten **önce** gelir |
| A11y (#15) | `SemanticsTester`, kontrast, tap target ≥ 48dp | Store dağıtımı yapılan uygulamalarda anlamlı |
| Perf (#13) | `flutter drive --profile` frame timing | Jank bütçesi |

---

## 2. Architecture fitness (docs/04 §2)

Flutter'da katman ihlali en sık görülen ajan hatası: UI'dan doğrudan repository/HTTP çağrısı.

```yaml
# analysis_options.yaml (dart_code_metrics)
dart_code_metrics:
  rules:
    - banned-usage:
        entries:
          - paths: ["lib/domain/**"]
            deny: ["package:http", "package:dio", "package:flutter/material.dart"]
            severity: error
          - paths: ["lib/presentation/**"]
            deny: ["package:sqflite", "package:http"]
            severity: error
    - avoid-cyclic-dependencies
```

Katman yönü: `domain ← application ← data ← presentation`. Domain hiçbir şeye bağımlı olamaz — Flutter'a bile.

---

## 3. Golden testleri — kısıtlı kullanım (ZORUNLU disiplin)

| ✅ Kullan | ❌ Kullanma |
|---|---|
| Stabil tasarım sistemi bileşenleri (buton, chip, kart) | **Ekran seviyesinde** — pixel diff cehennemi |
| Tek durumlu, animasyonsuz widget'lar | Animasyonlu / zamana bağlı widget |
| | Platform-bağımlı font render eden ekranlar |

Zorunlu ayarlar:
- Piksel eşiği ayarlanabilir yap → platform farkı gürültüsünü tolere et
- CI ve lokal aynı Flutter sürümü (font render sürüm bazlı değişir)
- Golden baseline değişikliği **Designer onayı** gerektirir (`docs/05` §1)

> **Öncelik kuralı:** Design token diff (renk/spacing/tipografi sabitleri) golden'dan
> **çok daha ucuz ve stabildir.** Önce onu kur (`docs/02` §5 sıra 18).

---

## 4. Yüksek çekişmeli dosyalar (docs/03 §6)

| Dosya | Politika |
|---|---|
| `pubspec.yaml` / `pubspec.lock` | `agent:deps` tek sahip · aynı bağımlılık PR'ında atomik commit · CI temiz çözümlemenin aynı lockfile'ı verdiğini doğrular |
| `*.g.dart`, `*.freezed.dart` | ADR ile tek strateji: CI üretimi veya sabit toolchain ile atomik commit; iki model karıştırılmaz |
| `lib/l10n/*.arb` | ARB parser ile yinelenen anahtar/şema kontrolü + tek sahip veya kısa lease; otomatik union yok |
| Route tablosu (`app_router.dart`) | Auto-discovery / kod üretimi tercih et; manuel ise tek sahip + semantik duplicate/ordering kontrolü |
| DI kaydı (`injection.dart`) | Aynı — `get_it` manuel kaydı yerine `injectable` kod üretimi |
| `ios/Podfile.lock` | `agent:deps` |
| `ios/Runner.xcodeproj/project.pbxproj` | Tek sahip · ayrı PR (merge kâbusu) |
| `android/app/build.gradle` | Tek sahip · ayrı PR |
| `design/tokens/**` | `agent:designer` + insan Designer |

> `*.g.dart` için stratejiyi repo çapında tekleştirmek esastır. Commit etmeme
> modeli yalnız CI'ın aynı toolchain ile deterministik üretim yaptığı projelerde
> güvenlidir.

---

## 5. Impact analysis (docs/04 §5)

Dart'ta hazır bir `--findRelatedTests` yok. Pratik yaklaşımlar:

- Dosya→test isim konvansiyonu (`lib/foo/bar.dart` → `test/foo/bar_test.dart`) + `git diff` eşlemesi
- `dart test --coverage` çıktısından test↔dosya haritası üret, cache'le
- Paket/feature bazlı bölme: değişen feature dizininin testlerini koş
- `codebase-memory-mcp → trace_path(mode=calls)`

Fast lane'de tam suite yerine bu alt kümeyi koş.

---

## 6. Fast lane komutu (docs/06 §1)

```bash
# hedef pilot baseline'ından türetilen repo p95 SLO'su
dart analyze --fatal-infos \
  && dart run dart_code_metrics:metrics check-unused-code lib \
  && <fitness-check> \
  && <criteria-coverage-check> \
  && flutter test <impact-selected-paths>
```

`build_runner`'ı fast lane'de koşuyorsan `--delete-conflicting-outputs` ile ve cache'le — yoksa süre patlar.

---

## 7. Flutter'a özgü anti-pattern'ler

| ❌ | Neden |
|---|---|
| Ekran seviyesinde golden test | Pixel diff cehennemi, sürekli kırılır |
| Generated dosya stratejilerini aynı repoda karıştırmak | En yaygın Flutter ajan çakışması ve drift kaynağı |
| `pumpAndSettle` yerine sabit `Duration` beklemek | Flake üretir → ajana test zayıflatmayı öğretir |
| Widget testinde gerçek HTTP | Yavaş + flaky; client'ı fake'le, widget ağacını gerçek tut |
| Her widget'ı mock'layıp "widget test" demek | Dikişi test etmez |
| `domain/` içinde `material.dart` import etmek | Katman ihlali — fitness function kırar |
| Design token'ı hardcode etmek (`Color(0xFF...)`) | Token diff'i anlamsız kılar |
| Tek `test/` dizinine her şeyi atmak | Taksonomi kaybolur, ajan baskın deseni kopyalar |
