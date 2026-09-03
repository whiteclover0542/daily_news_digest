# 배포 환경

## 결정

| 영역 | 선택 | 이유 |
|---|---|---|
| 프론트엔드 | **Vercel** | React/Next.js PWA 배포 표준, 무료 티어로 충분, 자동 HTTPS/도메인 |
| 백엔드 (API) | **Render** (Web Service, Free) | Railway는 무료 플랜이 폐지되어 최소 과금 발생. Render 무료 웹 서비스는 계속 무료(단, 15분 미사용 시 슬립 → 첫 요청 콜드스타트 30~50초) — 개인 포트폴리오 트래픽 수준에서 감수 가능 |
| DB | **Neon** (PostgreSQL, Free) | Render의 무료 PostgreSQL은 생성 후 30일 뒤 만료·삭제됨 — 계속 살아있어야 하는 포트폴리오 앱에는 부적합. Neon은 서버리스 PostgreSQL로 무료 티어가 기간 제한 없이 유지됨. Render 백엔드에서 Neon 커넥션 문자열로 연결 |

## 참고 — 스케줄러에 대한 영향

Render 무료 웹 서비스는 미사용 시 슬립 상태가 되므로, 백엔드 프로세스 내부에서 도는 APScheduler는 새벽 시간대에 서비스가 잠들어 있으면 실행되지 않을 수 있음. **GitHub Actions cron**으로 파이프라인 스크립트를 직접 실행하는 방식으로 결정한다.

- KST 오전 6시: 전날 이후 새 자료를 수집·요약해 오전 7시 브리핑을 준비
- KST 오후 1시: 당일 새로 게시된 보도자료를 보강 수집
- GitHub Actions cron은 UTC 기준이므로 각각 전날 21:00 UTC, 당일 04:00 UTC로 설정

## TODO (배포 시점에 진행)

- [x] Render 웹 서비스 생성 & 환경변수 설정 — render.yaml Blueprint, branch: dev
- [x] Neon 프로젝트 생성 & 커넥션 문자열 발급 — 통합 브랜치 pooled 커넥션 사용
- [x] Vercel 프로젝트 연결 (frontend 레포/폴더) — vercel CLI로 생성, production 배포 완료
- [x] 프론트 → 백엔드 API 호출 CORS 설정 — CORS_ORIGINS에 Vercel 프로덕션 도메인 추가, 응답 헤더로 확인
- [x] HTTPS/도메인 확인 (둘 다 기본 제공 도메인으로 충분, 커스텀 도메인은 선택) — 둘 다 https 기본 도메인으로 정상 접속 확인

## 배포 URL

| 영역 | URL |
|---|---|
| 프론트엔드 (Vercel) | https://frontend-kohl-ten-uqrg4vvv18.vercel.app |
| 백엔드 API (Render) | https://daily-news-digest-api.onrender.com |
| 헬스체크 | https://daily-news-digest-api.onrender.com/health |
