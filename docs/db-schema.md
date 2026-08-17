# DB 스키마

작성 예정. DB 종류(PostgreSQL vs MongoDB) 확정 후 아래 테이블/컬렉션 구조를 채운다.

## 테이블 (초안)

### articles (뉴스 기사)

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | PK | |
| title | string | 원문 제목 |
| source | string | 언론사 |
| url | string | 원문 링크 |
| category | string | 분류된 카테고리 |
| summary | text | LLM 요약 |
| keywords | string[] | 추출 키워드 |
| published_at | datetime | 원문 발행일 |
| collected_at | datetime | 수집 시각 |

### categories (카테고리)

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | PK | |
| name | string | 카테고리명 (정치/경제/IT/스포츠/문화 등) |

> 로그인/사용자 계정, 관심 카테고리 구독 기능은 없음. 알림 설정(확장 기능)은 로그인 없이(예: 이메일 주소만으로) 동작하는 구조로 설계.
