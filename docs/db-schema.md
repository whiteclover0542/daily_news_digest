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

> 로그인/사용자 계정, 관심 카테고리 구독 기능은 없음. 알림 설정(확장 기능)은 로그인 없이(예: 이메일 주소만으로) 동작하는 구조로 설계 예정 — 별도 `email_subscriptions(email)` 테이블 정도로 충분, MVP 이후 착수.
