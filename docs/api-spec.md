# API 명세

## 컨벤션

- Base URL: `/api` (배포 환경 확정 후 도메인 붙일 예정, 로컬 개발은 `http://localhost:8000/api`)
- 응답 포맷: JSON
- 인증: 없음 (로그인/계정 기능 자체를 두지 않음)
- 날짜/시간: ISO 8601, KST(+09:00) 기준
- 에러 응답: `{ "detail": "에러 메시지" }` (FastAPI 기본 형식)

## 엔드포인트

### GET /news — 오늘의 뉴스 목록 조회

**Query Parameters**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| category | string | N | 없음(전체) | 카테고리 slug (예: `economy`) |
| date | string (YYYY-MM-DD) | N | 오늘 날짜 | 조회할 날짜 (published_at 기준) |
| page | int | N | 1 | 페이지 번호 |
| limit | int | N | 20 | 페이지당 개수 (최대 50) |

**Response 200**

```json
{
  "date": "2026-08-18",
  "total": 42,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 101,
      "title": "기사 제목",
      "source": "언론사명",
      "category": { "id": 2, "name": "경제", "slug": "economy" },
      "summary_preview": "요약 앞부분 미리보기 (약 80자)",
      "published_at": "2026-08-18T07:12:00+09:00"
    }
  ]
}
```

정렬: `published_at` 내림차순(최신순) 고정.

### GET /news/{id} — 뉴스 상세 조회

**Path Parameters**: `id` (int)

**Response 200**

```json
{
  "id": 101,
  "title": "기사 제목",
  "source": "언론사명",
  "url": "https://example.com/article/101",
  "category": { "id": 2, "name": "경제", "slug": "economy" },
  "summary": "요약 전문",
  "keywords": ["금리", "환율"],
  "published_at": "2026-08-18T07:12:00+09:00",
  "collected_at": "2026-08-18T05:00:00+09:00"
}
```

**Response 404**: 해당 id의 기사가 없을 때 — `{ "detail": "Article not found" }`

### GET /categories — 카테고리 목록 조회

**Response 200**

```json
[
  { "id": 1, "name": "정치", "slug": "politics" },
  { "id": 2, "name": "경제", "slug": "economy" },
  { "id": 3, "name": "IT", "slug": "it" },
  { "id": 4, "name": "스포츠", "slug": "sports" },
  { "id": 5, "name": "문화", "slug": "culture" }
]
```

### POST /subscriptions/push — 웹 푸시 구독 등록

브라우저 `PushManager.subscribe()` 결과를 그대로 전달. 이미 등록된 endpoint면 키만 갱신(멱등).

**Request Body**

```json
{
  "endpoint": "https://fcm.googleapis.com/fcm/send/...",
  "keys": { "p256dh": "...", "auth": "..." }
}
```

**Response**: 204 No Content

### POST /subscriptions/push/unsubscribe — 웹 푸시 구독 해지

**Request Body**

```json
{ "endpoint": "https://fcm.googleapis.com/fcm/send/..." }
```

**Response**: 204 No Content
**Response 404**: 해당 endpoint로 등록된 구독이 없을 때 — `{ "detail": "Subscription not found" }`

---

> 확장 기능(검색, 트렌드) 엔드포인트는 MVP 이후 추가. (관심 카테고리 구독 기능은 없음)
> 실제 알림 발송은 REST 엔드포인트가 아니라 `app/services/push.py`의 `send_push_to_all()` + `scripts/send_push.py`(수동 트리거)로 구현. "매일 아침 자동 발송"은 스케줄러가 이 함수를 호출하도록 붙이는 일만 남음.
