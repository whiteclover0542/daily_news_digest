# whiteclover TODO

> 할 일 목록은 맨 위에서 관리하고, 그 아래 날짜별로 오늘 목표 / 오늘 한 일을 기록합니다 (최신순 정렬).

## 할 일

1. 배포 환경 구축 (Vercel + Render + Neon) — Neon은 완료. PR #25가 dev에 머지되기 전까진 Render/Vercel 둘 다 기본 브랜치(dev/main)에 backend·frontend 코드가 없어서 빌드 실패함 — PR 머지 후 이어서 진행하거나, 급하면 두 서비스 다 Branch를 whiteclover로 임시 지정해서 배포
2. HTTPS / 도메인 설정
3. 알림 발송 로직 — 로그인 없이 이메일 등록 방식 등 검토 (웹 푸시 / 이메일)
4. 알림 설정 화면
5. 키워드 트렌드 시각화 화면
6. 검색 API
7. 검색 화면

---

## 2026-08-18

### 오늘 목표
- 1. DB 종류/스키마 확정
- 2. API 명세 확정
- 3. 배포 환경 선정
- 4. GitHub Issues 등록
- 5. DB 모델 정의 & 적재 로직
- 6. 뉴스 목록/상세 API, 카테고리 API 구현
- 7. PR 올리기 (#25)
- 8. 프론트엔드 메인/상세 화면 + PWA 설정

### 오늘 한 일
- DB 종류 PostgreSQL로 확정 (관계형 데이터 구조 + FastAPI/SQLAlchemy 궁합)
- docs/db-schema.md 구체화: articles, categories, keywords, article_keywords 테이블 설계
- docs/api-spec.md 구체화: /news(쿼리 파라미터·페이지네이션), /news/{id}, /categories 응답 형식 확정
- 배포 환경 확정: Vercel(프론트) + Render(백엔드, Railway는 무료 플랜 폐지로 제외) + Neon(DB, Render 무료 Postgres는 30일 후 만료되어 제외) — docs/deployment.md
- 스케줄러 관련 주의사항 기록 (Render 무료 티어 슬립 → GitHub Actions cron 권장, hoya와 논의 필요)
- 라벨 8개 + 이슈 24개(#1~#24) gh CLI로 일괄 등록 (docs/github-issues-draft.md 기준). 로그인용 토큰은 저장소 한정·Issues 권한만·7일 만료 fine-grained PAT 사용 후 즉시 로그아웃/삭제
- GitHub Projects 보드 생성 (Todo/In Progress/In Review/Done) 및 이슈 24개 연결
- backend/app/core(config, database), backend/app/models(Article, Category, Keyword, article_keywords) 구현 + upsert_article 적재 헬퍼(crud.py, url 유니크 기준 중복 방지) 작성
- requirements.txt 작성, SQLite 인메모리로 스모크 테스트 통과 확인 (Python 3.12 로컬 설치)
- app/api(news.py, categories.py), app/schemas(news.py, category.py), app/services/news.py, app/main.py 구현
- 로컬에 Python 3.12 설치, 더미 데이터 시딩 스크립트(scripts/seed_dev_data.py) 작성 후 실제 서버 구동해 /api/news, /api/news/{id}, /api/categories 전부 curl로 동작 확인
- 테스트 중 실제 버그 발견 및 수정: "오늘" 필터가 KST가 아니라 UTC 기준으로 걸려서 정상 기사가 목록에서 빠지는 문제 → KST 하루 구간을 UTC로 변환해 바인딩하도록 수정 (SQLite의 DateTime이 tz-aware 값을 자동 변환하지 않는 것도 함께 확인)
- progress.md 0-3, 0-4 🔵(리뷰 중), 0-5 ✅, 0-6 ✅, ④ DB 적재 🔵(리뷰 중), ⑤ 뉴스/카테고리 API ✅ 로 갱신
- PR #25 생성 (whiteclover → dev), commit 2개(docs, feat)로 정리해서 push
- 프론트엔드 결정: Vite + React + TypeScript (Next.js 대비 서버 기능이 필요 없고 유지보수 부담이 적어서 선택)
- Vite+React+PWA 스캐폴딩, react-router-dom으로 메인/상세 라우팅, api/client.ts로 백엔드 연동
- 메인 화면(카테고리 탭 + 뉴스 카드), 상세 화면(요약/키워드/원문링크) 구현
- vite-plugin-pwa로 manifest + 서비스워커 설정 (PWA 항목까지 함께 완료)
- 백엔드에 CORS 미들웨어 빠져있던 것 발견해서 추가 (프론트-백엔드 다른 포트라 필요)
- 실제 백엔드+프론트 같이 띄우고 헤드리스 Edge로 스크린샷 찍어서 목록/카테고리 필터/상세 화면 렌더링 확인
- progress.md ⑥ 프론트엔드(메인/상세/PWA) 전부 ✅ 로 갱신
