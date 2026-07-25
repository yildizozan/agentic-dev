Aşağıdaki dokümanı Hermes için **genel (generic) agentic software development framework tasarımı** olarak hazırladım. Lumie, Falista, Unity oyunları veya başka herhangi bir yazılım projesine uygulanabilir.

Odak noktası:

* Agent profilleri
* Workflow mimarisi
* Orchestrator
* Repository yapısı
* Issue → Workflow → Agent → Artifact → Commit zinciri
* Devil's Advocate
* Release Engineer
* Deterministic execution yaklaşımı

---

# Hermes Agentic Engineering Framework

## 1. Amaç

Hermes'in amacı:

> İnsan yazılım ekiplerinin çalışma modelini agent tabanlı yapay zeka ekiplerine dönüştürmek.

Hermes bir "chatbot" değildir.

Hermes:

* projeyi anlayan,
* görevleri planlayan,
* doğru agent'ı seçen,
* standart workflow çalıştıran,
* çıktıları denetleyen,
* kaliteli yazılım üreten

bir **AI engineering operating system** yaklaşımıdır.

---

# 2. Temel Felsefe

Klasik yazılım geliştirme:

```
İnsan
 |
Kod
 |
Build
 |
Deploy
```

---

Basit AI kullanımı:

```
İnsan
 |
LLM
 |
Kod
```

Problemi:

* tekrar üretilebilirlik yok
* kalite değişken
* audit zor
* hata analizi zor

---

Hermes yaklaşımı:

```
İnsan
 |
Issue
 |
Workflow
 |
Agent Team
 |
Artifacts
 |
Review
 |
Commit
 |
Release
```

LLM burada:

> Sistemin tamamı değil, sistem içindeki uzman çalışanlardan biridir.

---

# 3. Hermes'in 4 Ana Katmanı

Hermes dört temel parçadan oluşur.

```
                  HERMES

        +-----------------------+
        |       Profiles        |
        |   (Agent kimliği)     |
        +-----------------------+

        +-----------------------+
        |      Workflows        |
        | (İş yapma prosedürü)  |
        +-----------------------+

        +-----------------------+
        |     Orchestrator      |
        |  (Yönetici sistem)    |
        +-----------------------+

        +-----------------------+
        |      Artifacts        |
        |  (Üretilen bilgi)     |
        +-----------------------+
```

---

# 4. Agent Profile Nedir?

Profile:

> Bir agent'ın kim olduğunu, ne bildiğini ve nasıl davranacağını tanımlar.

Örnek:

```
Flutter Engineer
```

Bu bir workflow değildir.

Bu sadece çalışandır.

---

Bir profile şunları içerir:

```
Identity

Responsibilities

Skills

Tools

Rules

Forbidden Actions

Expected Output
```

---

Örnek:

```
flutter-engineer.md
```

```markdown
# Flutter Engineer


## Role

Flutter uygulamalarının geliştirilmesinden sorumludur.


## Responsibilities

- UI geliştirme
- State management
- Navigation
- Flutter testleri


## Must Do

- Kod değişikliği öncesi architecture oku
- Test yaz
- Static analysis çalıştır


## Must Not Do

- Backend mimarisi değiştirme
- Güvenlik kararları verme


## Output

- Source code
- Tests
- Implementation notes
```

---

# 5. Hermes Agent Rolleri

İdeal generic ekip:

```
                    Hermes Team


                      Director
                         |
                         |
                  Project Manager
                         |
        +----------------+----------------+
        |                                 |
 Product Designer                  Tech Lead
                                         |
          +--------------+---------------+
          |              |               |
    Frontend         Backend          QA
    Engineer         Engineer       Engineer

                         |
                  Security Engineer

                         |
                Devil's Advocate

                         |
                Release Engineer
```

---

# 6. Roller ve Sorumlulukları

---

# 6.1 Project Manager Agent

## Görevi

İş ihtiyacını teknik göreve dönüştürür.

İnsan product owner yerine çalışır.

---

Input:

```
User request
```

Output:

```
Engineering task
```

---

Sorumluluklar:

* Issue oluşturma
* Requirement analizi
* Acceptance criteria
* Önceliklendirme
* Dependency belirleme

---

Yapmaz:

* Kod yazmaz
* Teknik mimari belirlemez

---

Örnek:

Input:

```
Google login ekle
```

Output:

```
Feature:

Google Authentication

Requirements:

- User can login
- Existing users preserved
- Error handling

Dependencies:

- Firebase Auth
- UI update
```

---

# 6.2 Product Designer Agent

## Görevi

Kullanıcı deneyimini tasarlar.

---

Sorumluluk:

* User flow
* UX kararları
* UI specification
* Design consistency

Output:

```
design-spec.md
```

Örnek:

```yaml
screen:

Login

states:

loading
error
success

components:

EmailInput
PasswordInput
LoginButton
```

---

# 6.3 Tech Lead Agent

Hermes'in en kritik rolüdür.

Görevi:

> Teknik doğruluğu korumak.

Sorumluluk:

* Architecture
* ADR
* Technical decision
* Code review

Output:

```
architecture.md

ADR.md
```

---

Yapmaz:

* Her şeyi kendi yazmaz
* Developer yerine geçmez

---

# 6.4 Software Engineer Agent

Örneğin:

* Flutter Engineer
* Backend Engineer
* Unity Engineer

Görevi:

Planı uygular.

---

Input:

```
Architecture
Design
Requirements
```

Output:

```
Code

Tests

Documentation
```

---

# 6.5 QA Engineer Agent

Görevi:

Kaliteyi garanti etmek.

Sorumluluk:

* Test plan
* Regression
* Automation
* Bug discovery

Output:

```
test-plan.md

test-results.md
```

---

QA koddan sonra değil:

Workflow'un parçasıdır.

---

# 6.6 Security Engineer Agent

Görevi:

Güvenlik kontrolü.

Kontrol eder:

* Authentication
* Authorization
* Secrets
* Dependency
* API exposure
* Data protection

Output:

```
security-review.md
```

---

# 6.7 Devil's Advocate Agent

Bu agent özellikle önemlidir.

Görevi:

> Sistemdeki herkesin kararlarını sorgulamak.

Pozitif üretmez.

Eleştirir.

---

Örnek:

Tech Lead:

```
Firestore kullanacağız.
```

Devil:

```
Risk:

100K kullanıcı sonrası query cost artabilir.

Öneri:

Index strategy oluştur.
```

---

Kontrol eder:

## Architecture attack

* Ölçeklenebilir mi?
* Yanlış teknoloji mi?

## Code attack

* Edge case var mı?
* Bug riski?

## Product attack

* Kullanıcı bunu ister mi?

---

Output:

```
risk-report.md
```

---

# 6.8 Release Engineer Agent

Görevi:

Kodun production'a güvenli gitmesini sağlamak.

Sorumluluk:

* Build
* CI/CD
* Migration
* Deployment
* Rollback

Kontrol:

```
Code

↓

Build

↓

Test

↓

Security

↓

Deploy

↓

Monitor
```

---

Output:

```
release-report.md
```

---

# 7. Workflow Nedir?

Workflow:

> Bir işin nasıl tamamlanacağını tanımlayan süreçtir.

Profile:

```
Kim?
```

Workflow:

```
Nasıl?
```

---

Örnek:

Profile:

```
Flutter Engineer
```

Workflow:

```
Feature Development
```

---

# 8. Workflow Yapısı

Workflow generic olmalıdır.

Örnek:

```
workflows/

feature-development.yaml

bug-fix.yaml

security-review.yaml

release.yaml
```

---

Feature workflow:

```yaml
name: feature-development


steps:

- product-analysis

- design

- architecture

- implementation

- testing

- security-review

- devil-review

- release-review
```

---

# 9. Repository Yapısı

İdeal yapı:

```
project/

src/


.hermes/

    profiles/

    workflows/

    policies/

    context/

    artifacts/

```

---

## profiles

Agent tanımları

---

## workflows

İş süreçleri

---

## policies

Kurallar

Örnek:

```
No merge without QA

Security required for auth changes
```

---

## context

Proje hafızası

Örnek:

```
architecture.md

coding-rules.md

database-schema.md
```

---

## artifacts

Agent çıktıları

```
issue-123/

    design.md

    architecture.md

    test-report.md

    security-report.md
```

---

# 10. Issue Nasıl Çalışır?

Issue:

Workflow tetikleyicisidir.

Örnek:

GitHub Issue:

```
Title:

Add Google Login


Type:

Feature


Workflow:

feature-development
```

---

Hermes:

```
Issue

↓

Workflow seç

↓

Agent dağıt

↓

Çıktıları topla

↓

Review

↓

Commit
```

---

# 11. Workflow Nerede Tutulur?

İdeal:

İki seviye:

## Global Hermes Repository

```
hermes/

workflows/

feature.yaml
bugfix.yaml
```

Genel standart.

---

## Proje Repository

```
my-app/

.hermes/8dDPdDySQEsOFCx4i1nnkmArRtLs6YPDkoG05i6S4aQf0tIDDMmjNBoESJdCdbSXS2h39VsjKobRYuzb

workflows/

feature.yaml
```

Proje özelleştirmesi.

---

# 12. Workflow Versioning

Çok önemli.

Yanlış:

```
feature.yaml değiştir
```

---

Doğru:

```
feature-v1.yaml

feature-v2.yaml
```

---

Çünkü:

Bugün yapılan issue:

```
workflow=v1
```

ile çalışmıştır.

Yarın:

```
workflow=v2
```

kullanılır.

---

# 13. Git Commit Standardı

Commit:

```
feat(auth): add google login


Hermes:

Issue:
#123

Workflow:
feature-v2

Agent:
flutter-engineer8dDPdDySQEsOFCx4i1nnkmArRtLs6YPDkoG05i6S4aQf0tIDDMmjNBoESJdCdbSXS2h39VsjKobRYuzb
```

---

Böylece:

Kim yaptı?

Hangi süreç?

Hangi karar?

bilinir.

---

# 14. Tool Gerekiyor mu?

Başlangıç:

Hayır.

Yeterli:

```
Git

YAML

Hermes Runner
```

---

Büyüyünce:

Workflow engine:

* Temporal
* Argo Workflow
* Prefect
* Dagster

kullanılabilir.

---

# 15. İdeal Hermes Akışı

Tam akış:

```
Human

 |

Issue

 |

Project Manager

 |

Workflow Selection

 |

Product Designer

 |

Tech Lead

 |

Engineers

 |

QA

 |

Security

 |

Devil's Advocate

 |

Release Engineer

 |

Pull Request

 |

Merge

 |

Production

```

---

# Son Mimari Prensip

Hermes'in temel prensibi:

```
LLM özgür düşünür.

Workflow sınırlar.

Agent uzmanlaşır.

Artifact hafızayı oluşturur.

Git geçmişi garanti eder.

```

Böylece:

* AI rastgele çalışan bir chatbot olmaktan çıkar.
* Tekrarlanabilir bir yazılım organizasyonuna dönüşür.

Bu yapı küçük bir proje için bile çalışır, ancak yüzlerce agent ve onlarca projeye ölçeklenebilecek şekilde tasarlanmıştır.

