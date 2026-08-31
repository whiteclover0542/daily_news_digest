# whiteclover TODO

> 할 일 목록은 맨 위에서 관리하고, 그 아래 날짜별로 오늘 목표 / 오늘 한 일을 기록합니다 (최신순 정렬).

## 할 일

1. 알림 발송 로직 — 백엔드 구독/해지 API, 실제 발송 함수(`send_push_to_all`)까지 완료. 남은 것: 콘텐츠 파이프라인·스케줄러 완성되면 그 트리거에서 이 함수를 호출하도록 연결
2. 알림 설정 화면 — 프론트에서 구독 API 붙여서 켜기/끄기 UI, 서비스워커 push 이벤트 핸들러
3. 키워드 트렌드 시각화 화면
4. 검색 API
5. 검색 화면

---

## 2026-08-20

### 오늘 목표
- PR #25 머지 후 배포 환경 구축 마무리 (Render + Vercel)

### 오늘 한 일
- PR #25(whiteclover → dev) 머지 확인, 로컬 dev/whiteclover 브랜치 동기화
- Render Blueprint(render.yaml) 작성 — rootDir/build/start command 자동화, branch는 dev로 고정
- Render 배포 중 `CORS_ORIGINS` 파싱 에러 발생 — pydantic-settings가 `list[str]` 필드는 field_validator보다 먼저 JSON 디코딩을 시도한다는 걸 확인, `NoDecode` 어노테이션으로 우회해서 콤마 구분 문자열을 받도록 수정 (로컬 임시 venv로 재현·검증 후 배포)
- Render 배포 성공, 다만 `/api/news`·`/api/categories`가 500 — Neon(통합 브랜치)엔 테이블이 없었던 것(마이그레이션 도구 없이 seed 스크립트로만 테이블 생성했는데 로컬 SQLite에만 실행해봤음)이 원인. 로컬에서 Neon 통합 브랜치 대상으로 `scripts/seed_dev_data.py` 실행해 테이블 생성 + 더미 기사 2건 시딩, API 정상 응답 확인
- 공용 PC에서 DB 커넥션 문자열을 PowerShell에 직접 입력한 것 인지 → PSReadLine 히스토리 파일에 평문으로 남는 문제 확인, 삭제 안내
- Vercel CLI로 frontend 프로젝트 생성·연결, `VITE_API_BASE_URL`(production/preview) 환경변수 등록, production 배포
- Render `CORS_ORIGINS`에 Vercel 프로덕션 도메인 추가, curl로 실제 Origin 헤더 넣어 `access-control-allow-origin` 정상 응답 확인
- progress.md 배포 환경 구축·HTTPS/도메인 항목 ✅ 로 갱신
- 배포 핫픽스 4개 커밋을 PR 없이 dev에 바로 올렸던 것을 발견 → dev에서 되돌리고(3b24738), whiteclover 브랜치에 그대로 남겨서 정식 PR로 다시 올릴 수 있게 정리(158d17b). 이미 배포된 Render/Vercel 서비스 자체는 git 히스토리와 무관하게 계속 정상 동작 중
- 알림 발송 방식 결정: 이메일 대신 웹 푸시 — PWA에 서비스워커가 이미 있어서 이메일 발송 계정 없이 자체 VAPID 키만으로 구현 가능
- `push_subscriptions` 모델(endpoint/p256dh/auth) 추가, `subscribe_push`(endpoint 중복 시 키만 갱신하는 멱등 처리)·`unsubscribe_push` CRUD 헬퍼 작성
- `POST /api/subscriptions/push`, `POST /api/subscriptions/push/unsubscribe` API 구현, main.py에 라우터 연결 + CORS `allow_methods`에 POST 추가
- docs/db-schema.md, docs/api-spec.md에 push_subscriptions 테이블·API 명세 반영
- `app/services/push.py`(send_push_to_all) 구현 — pywebpush로 구독자 전원 발송, 404/410(만료) 응답 오는 구독은 자동 삭제. 수동 트리거용 `scripts/send_push.py`도 추가 (스케줄러 붙기 전까지 CLI로 발송 테스트)
- VAPID 키 로컬에서 `npx web-push generate-vapid-keys`로 발급, config.py에 VAPID_PUBLIC_KEY/PRIVATE_KEY/SUBJECT 설정 추가
- webpush 함수를 mock해서 정상 발송 1건 + 만료(410) 구독 자동 정리 1건 동작 로컬 검증

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
