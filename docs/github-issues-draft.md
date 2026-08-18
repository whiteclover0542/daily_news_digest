# GitHub Issues 등록용 초안

progress.md 기준으로 아직 시작 전(⬜)이거나 진행 중(🔵)인 작업을 이슈 단위로 정리. GitHub에서 이 목록대로 Issue를 생성하고, Projects 보드(Todo / In Progress / In Review / Done 컬럼)에 담으면 됨.

라벨 제안: `backend`, `frontend`, `pipeline`, `ai`, `infra`, `docs`, `mvp`, `extension`

---

## 공통/기반

- [ ] **뉴스 소스 조사 (RSS vs API)** — 담당: hoya · 라벨: `pipeline`, `docs`
  기획서 12장 체크리스트. RSS 피드 vs 뉴스 API 비교 후 결정.

- [ ] **API 명세 리뷰** — 담당: hoya (리뷰) · 라벨: `docs`
  whiteclover가 작성한 docs/api-spec.md 리뷰 및 확정.

- [ ] **DB 스키마 리뷰** — 담당: hoya (리뷰) · 라벨: `docs`
  whiteclover가 작성한 docs/db-schema.md 리뷰 및 확정.

## MVP

- [ ] **수집기 구현 (RSS/API)** — 담당: hoya · 라벨: `pipeline`, `mvp`
  backend/pipeline/collectors

- [ ] **스케줄러 구현** — 담당: hoya · 라벨: `pipeline`, `mvp`
  backend/pipeline/scheduler — Render 슬립 이슈로 GitHub Actions cron 검토 (docs/deployment.md 참고)

- [ ] **전처리 로직 구현** — 담당: hoya · 라벨: `pipeline`, `mvp`
  backend/pipeline/preprocessing — 중복 기사 제거, 광고성 텍스트 필터링

- [ ] **LLM 요약/카테고리 분류 로직** — 담당: hoya · 라벨: `ai`, `mvp`
  backend/ai

- [ ] **DB 모델 정의 & 적재** — 담당: hoya·whiteclover · 라벨: `backend`, `mvp`
  backend/app/models — docs/db-schema.md 기준 SQLAlchemy 모델

- [ ] **뉴스 목록/상세 API 구현** — 담당: whiteclover · 라벨: `backend`, `mvp`
  GET /news, GET /news/{id} — docs/api-spec.md 기준

- [ ] **카테고리 API 구현** — 담당: whiteclover · 라벨: `backend`, `mvp`
  GET /categories

- [ ] **메인 화면 (PWA)** — 담당: whiteclover · 라벨: `frontend`, `mvp`
  카테고리 탭 + 뉴스 카드 리스트

- [ ] **상세 화면 (PWA)** — 담당: whiteclover · 라벨: `frontend`, `mvp`
  요약 전문 + 키워드 + 원문 링크

- [ ] **PWA 설정** — 담당: whiteclover · 라벨: `frontend`, `mvp`
  manifest, 서비스워커

## 확장 기능

- [ ] **알림 발송 로직 (웹 푸시/이메일)** — 담당: whiteclover · 라벨: `backend`, `extension`
- [ ] **알림 설정 화면** — 담당: whiteclover · 라벨: `frontend`, `extension`
- [ ] **키워드 집계 로직** — 담당: hoya · 라벨: `pipeline`, `extension`
- [ ] **키워드 트렌드 시각화 화면** — 담당: whiteclover · 라벨: `frontend`, `extension`
- [ ] **검색 API** — 담당: whiteclover · 라벨: `backend`, `extension`
- [ ] **검색 화면** — 담당: whiteclover · 라벨: `frontend`, `extension`

## 인프라/배포

- [ ] **Render 백엔드 배포 구축** — 담당: whiteclover · 라벨: `infra`
- [ ] **Neon DB 연결** — 담당: whiteclover · 라벨: `infra`
- [ ] **Vercel 프론트 배포 구축** — 담당: whiteclover · 라벨: `infra`
- [ ] **HTTPS/도메인 확인** — 담당: whiteclover · 라벨: `infra`
- [ ] **GitHub Actions cron 스케줄러 자동 실행 설정** — 담당: hoya · 라벨: `infra`, `pipeline`

---

## Projects 보드 컬럼 제안

`Todo` → `In Progress` → `In Review (PR)` → `Done`
(progress.md의 ⬜/🟡/🔵/✅ 상태와 1:1 매칭됨)
