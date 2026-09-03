# 뉴스 요약 앱 진행 로그 (PROGRESS)

> 팀원이 각자 작업 완료 시 직접 갱신하는 문서입니다.
> 상태 바뀌면 `docs: 진행로그 업데이트` 로 커밋해 주세요.
> **최종 수정:** 2026-08-20 (배포 완료 + 웹 푸시 알림 백엔드 착수 반영)

## 상태 표기
- ⬜ 시작 전  |  🟡 진행 중  |  🔵 리뷰 중(PR)  |  ✅ 완료  |  ⛔ 막힘(blocked)

---

## 📊 진행 현황 보기

| 영역 | 진행률 |
|------|--------|
| 프로젝트 기반 작업 (공통) | 🟡 3/6 (✅), 2개 🔵 리뷰 중 |
| MVP 핵심 기능 6개 | 🟡 2/6 (✅), 1개 🔵 리뷰 중 |
| 확장 기능 3개 | 🟡 0/3 (✅), 1개 🟡 진행 중 |

---

## 0. 프로젝트 기반 작업 (공통)

| # | 항목 | 담당 | 상태 | 비고 |
|---|------|------|------|------|
| 0-1 | Git 레포 생성 & 문서 정비 | 공통 | ✅ | 폴더 구조, 기획서, docs/ 문서 정비 |
| 0-2 | 뉴스 소스 조사 (RSS vs API) | hoya | ✅ | MVP 소스: 과학기술정보통신부 IT 보도자료. RSS로 새 자료를 찾고, 상세 페이지·공개 첨부 PDF/HWPX 전문을 수집해 요약 |
| 0-3 | DB 종류/스키마 확정 | 공통 | 🔵 | docs/db-schema.md — PostgreSQL로 확정, hoya 리뷰 필요 (PR #25) |
| 0-4 | API 명세 확정 | 공통 | 🔵 | docs/api-spec.md — /news, /news/{id}, /categories 상세화, hoya 리뷰 필요 (PR #25) |
| 0-5 | GitHub Issues/Projects 세팅 | 공통 | ✅ | 이슈 24개(#1~#24) + Projects 보드(Todo/In Progress/In Review/Done) 생성 완료 |
| 0-6 | 배포 환경 선정 | whiteclover | ✅ | Vercel(프론트) + Render(백엔드) + Neon(DB) — docs/deployment.md |

---

## 1. MVP 핵심 기능

### ① 뉴스 자동 수집 (스케줄러)
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 수집기 (RSS/API) | hoya | ⬜ | backend/pipeline/collectors |
| 스케줄러 | hoya | ⬜ | backend/pipeline/scheduler |

### ② 전처리 (정제·중복제거·필터링)
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 전처리 로직 | hoya | ⬜ | backend/pipeline/preprocessing |

### ③ LLM 요약 + 카테고리 분류
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 요약/분류 로직 | hoya | ⬜ | backend/ai |

### ④ DB 적재
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 모델 정의 & 적재 | hoya·whiteclover | ✅ | backend/app/models — Article/Category/Keyword 모델 + upsert_article 헬퍼 (PR #25) |

### ⑤ 백엔드 API
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 뉴스 목록/상세 API | whiteclover | ✅ | GET /news, GET /news/{id} — 실제 서버 구동해 동작 확인 완료 (PR #25) |
| 카테고리 API | whiteclover | ✅ | GET /categories — 동작 확인 완료 (PR #25) |

### ⑥ 프론트엔드 (PWA)
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 메인 화면 | whiteclover | ✅ | 카테고리 탭 + 뉴스 카드 리스트, 헤드리스 브라우저로 렌더링 확인 (PR #25) |
| 상세 화면 | whiteclover | ✅ | 요약 전문 + 키워드 + 원문 링크 (PR #25) |
| PWA 설정 | whiteclover | ✅ | vite-plugin-pwa로 manifest/서비스워커 설정 (PR #25) |

---

## 2. 확장 기능 (여유 있을 때)

### ⑦ 알림 (웹 푸시 / 이메일)
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 알림 발송 로직 | whiteclover | 🟡 | 웹 푸시로 결정(이메일 대신) — PWA 서비스워커가 이미 있어 별도 이메일 발송 계정 없이 자체 VAPID 키만으로 동작. `push_subscriptions` 모델, 구독/해지 API, `send_push_to_all()`(pywebpush, 만료 구독 자동정리) 구현·검증 완료. 남은 건 스케줄러가 이 함수를 호출하도록 연결하는 것뿐 |
| 설정 화면 | whiteclover | ⬜ | 프론트 구독 켜기/끄기 UI — 백엔드 API만 있고 아직 미착수 |

### ⑧ 키워드 트렌드 시각화
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 키워드 집계 로직 | hoya | ⬜ | |
| 시각화 화면 | whiteclover | ⬜ | |

### ⑨ 검색 기능
| 파트 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 검색 API | whiteclover | ⬜ | |
| 검색 화면 | whiteclover | ⬜ | |

---

## 3. 인프라 / 배포

| 항목 | 담당 | 상태 | 비고 |
|------|------|------|------|
| 배포 환경 구축 | whiteclover | ✅ | Render(백엔드, dev 브랜치) + Vercel(프론트, production) + Neon(통합 브랜치) 연결, CORS 설정 및 시딩 데이터로 API 동작 확인 완료 |
| 스케줄러 자동 실행 설정 | hoya | ⬜ | GitHub Actions cron 또는 APScheduler |
| HTTPS / 도메인 | whiteclover | ✅ | Render/Vercel 기본 도메인 HTTPS 자동 적용 확인 (커스텀 도메인 계획 없음) |

---

## 🔄 갱신 방법

1. 본인이 맡은 칸의 상태 이모지 수정 + 비고 기입
2. `git add docs/progress/progress.md`
3. `git commit -m "docs: 진행로그 업데이트 - <내용>"`
4. `git push`
