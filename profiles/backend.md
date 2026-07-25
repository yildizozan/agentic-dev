# Profil — Backend (HTTP servisleri)

> `docs/`'taki kurallara eşleme. Çelişki halinde `docs/` kazanır.

---

## 1. Test katmanı eşlemesi

| `docs/02` §3 katmanı | Araç |
|---|---|
| Contract (#2) | OpenAPI + `Spectral` (lint) + `oasdiff` (breaking gate) + `Schemathesis` (fuzz/contract) + `Pact` (CDC) |
| Statik (#3) | strict tip · linter · `dead-code` · dependency policy |
| Architecture fitness (#4) | `import-linter` (Py) · `dependency-cruiser` (TS) · `ArchUnit` (JVM) · `go-arch-lint` · `packwerk` (Ruby) |
| Integration (#5) | **Testcontainers** — gerçek DB/broker. In-memory taklit yalnız son çare. |
| Regresyon (#6) | Kilitli smoke set |
| Security (#7) | `Semgrep` custom rule (auth sınırı) · `Gitleaks` · `OSV-Scanner` · SBOM · authz contract (BOLA/BFLA) |
| Property-based (#8) | `Hypothesis` (Py) · `fast-check` (TS) · `jqwik` (JVM) — para, kota, state machine, idempotency |
| Mutation (#9) | `mutmut`/`cosmic-ray` (Py) · `Stryker` (TS) · `PIT` (JVM) — **incremental, diff'te** |
| E2E (#10) | API seviyesi uçtan uca, max 10 |
| Snapshot (#11) | API response snapshot (şema değil gövde) |
| Perf (#13) | `k6` — p95 latency bütçesi |

---

## 2. Contract testleri — interface freeze (docs/03 §3)

Multi-agent'ta en kritik backend kalemi. Sıralama **zorunlu**:

```
1. agent:techlead OpenAPI şemasını yazar        (contracts/)
2. Şema kendi PR'ında merge edilir              ← BARİYER
3. CI client/stub üretir                        (generated/, commit EDİLMEZ)
4. ANCAK ŞİMDİ backend + istemci ajanları paralel açılır
```

Gate'ler:
- `Spectral` → şema lint (fast lane)
- `oasdiff breaking` → breaking change tespiti → **G3 insan onayı** (merge lane)
- `Schemathesis` → şemadan otomatik fuzz; implementasyonun şemaya uyduğunu doğrular
- `Pact` → tüketici odaklı sözleşme; birden fazla istemci varsa

> **Anti-pattern:** OpenAPI şemasını CI'a bağlamamak. Bağlanmamış şema dekorasyondur
> (`docs/01` §1.1).

---

## 3. Impact analysis (docs/04 §5)

| Dil | Araç |
|---|---|
| Python | `pytest-testmon` · coverage-tabanlı test↔dosya haritası |
| TS/JS | `jest --findRelatedTests` · `nx affected` |
| .NET | `dotnet-affected` |
| JVM | Gradle test filtering + `test-retry` analizi |
| Go | `go test` + paket bağımlılık grafı |
| Genel | `codebase-memory-mcp → trace_path(mode=calls)` |

---

## 4. Property-based — nerede en yüksek getiri

| Alan | Invariant örneği |
|---|---|
| Para/fiyat | Toplam = kalemler toplamı · yuvarlama kaybı ≤ 1 kuruş · negatif tutar yok |
| Kota/limit | Hiçbir sırada limit aşılamaz |
| State machine | Geçersiz durum geçişi imkânsız · terminal durumdan çıkış yok |
| Idempotency | Aynı key ile 2. çağrı yeni yan etki üretmez |
| Sıralama/sayfalama | Sayfaların birleşimi = tüm set, kayıp/tekrar yok |
| Serileştirme | `decode(encode(x)) == x` |

---

## 5. Yüksek çekişmeli dosyalar (docs/03 §6)

| Dosya | Politika |
|---|---|
| `db/migrations/**` | **Timestamp/ULID isimlendirme** (sıralı numara = garantili çakışma) · daima kendi PR'ı · `agent:migration` · geri alınabilir |
| Lockfile'lar | `agent:deps` · feature PR'ında commit edilmez |
| `generated/**` (client, protobuf, ORM tipleri) | Commit edilmez, CI üretir |
| Route tablosu / DI container | Öncelik: **auto-discovery**. Mümkün değilse satır başına tek kayıt + `merge=union` |
| i18n / mesaj dosyaları | Satır başına tek anahtar, sıralı, `merge=union` + çakışma kontrolü |
| `openapi.yaml` | `agent:techlead` tek sahip |

---

## 6. Fast lane komutu (docs/06 §1)

```bash
# hedef < 3 dk — push etmeden önce yeşil olmalı
<typecheck> && <lint> && <fitness-check> && <secret-scan-diff> \
  && python3 tools/criteria_coverage.py \
  && <impact-selected-tests>
```

---

## 7. Backend'e özgü anti-pattern'ler

| ❌ | Neden |
|---|---|
| Şemayı paralel ajanlara tasarlatmak | İki farklı şema, işin yarısı çöpe (`docs/03` §3) |
| Migration'ı feature koduyla aynı PR'da | Garantili çakışma + geri alınamazlık |
| Sıralı migration numaralandırması | Her paralel ajan aynı numarayı alır |
| DB'yi mock'lamak | Gerçek hatalar dikişte — Testcontainers kullan |
| Repository'yi mock'layıp "integration test" demek | Unit test'tir, dikişi test etmez |
| Authz'ı yalnız happy path'te test etmek | BOLA/BFLA negatif senaryo zorunlu |
| OpenAPI'yi CI'a bağlamamak | Dekorasyon |
| Generated client'ı commit etmek | Çakışma + bayat kod |
