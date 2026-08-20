# DB 스키마

## DB 종류: PostgreSQL

카테고리별 필터링, 정형화된 컬럼(제목/언론사/URL/발행일 등) 위주라 관계형 모델이 자연스럽고, FastAPI + SQLAlchemy 조합과 Render/Railway 배포 지원도 좋아 PostgreSQL로 확정.

## 테이블

### categories (카테고리)

| 컬럼 | 타입 | 제약 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | |
| name | VARCHAR(30) | UNIQUE NOT NULL | 카테고리명 (정치/경제/IT/스포츠/문화 등) |
| slug | VARCHAR(30) | UNIQUE NOT NULL | URL/쿼리 파라미터용 영문 키 (politics, economy, it, sports, culture) |

초기 시드 데이터: 정치, 경제, IT, 스포츠, 문화 (5개, 이후 조정 가능)

### articles (뉴스 기사)

| 컬럼 | 타입 | 제약 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | |
| title | VARCHAR(300) | NOT NULL | 원문 제목 |
| source | VARCHAR(100) | NOT NULL | 언론사 |
| url | TEXT | UNIQUE NOT NULL | 원문 링크 (중복 수집 방지용 유니크 키) |
| category_id | INTEGER | FK → categories.id, NOT NULL | 분류된 카테고리 |
| summary | TEXT | NOT NULL | LLM 요약 |
| published_at | TIMESTAMPTZ | NOT NULL | 원문 발행일 |
| collected_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | 수집 시각 |

인덱스: `(category_id, published_at DESC)` — 카테고리별 오늘의 뉴스 목록 조회용

### keywords (추출 키워드)

| 컬럼 | 타입 | 제약 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | |
| word | VARCHAR(50) | UNIQUE NOT NULL | 키워드 원문 |

### article_keywords (기사-키워드 매핑, N:M)

| 컬럼 | 타입 | 제약 | 설명 |
|---|---|---|---|
| article_id | INTEGER | FK → articles.id | |
| keyword_id | INTEGER | FK → keywords.id | |

PK: `(article_id, keyword_id)` 복합키. 키워드를 별도 테이블로 분리해 확장 기능(⑧ 키워드 트렌드 시각화)에서 집계 쿼리(`GROUP BY keyword_id`)를 바로 활용할 수 있게 함.

> 로그인/사용자 계정, 관심 카테고리 구독 기능은 없음.

### push_subscriptions (웹 푸시 구독)

이메일 대신 브라우저 Web Push로 결정 — 이미 PWA(서비스워커)가 있어서 별도 이메일 발송 서비스 계정 없이 자체 발급 VAPID 키만으로 동작 가능.

| 컬럼 | 타입 | 제약 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | |
| endpoint | TEXT | UNIQUE NOT NULL | 브라우저가 발급한 푸시 엔드포인트 URL (구독 식별자) |
| p256dh | TEXT | NOT NULL | 구독 공개키 (Web Push 암호화용) |
| auth | TEXT | NOT NULL | 구독 인증 시크릿 |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | 구독 시각 |

발송 로직(`app/services/push.py`, 구독자 전원 순회 + `pywebpush`로 전송, 404/410 응답 오는 만료 구독은 자동 정리)은 구현 완료. 실행에 필요한 `VAPID_PUBLIC_KEY`/`VAPID_PRIVATE_KEY`/`VAPID_SUBJECT` 환경변수는 `.env.example` 참고, 실제 키는 로컬에서 `npx web-push generate-vapid-keys`로 생성.

수동 트리거: `python scripts/send_push.py "제목" "본문" [url]` — 스케줄러가 아직 없어서 로컬/CLI로 직접 실행. "매일 아침 자동 발송"은 콘텐츠 파이프라인·스케줄러 완성 후 그 트리거에서 이 함수를 호출하도록 연결 예정.
