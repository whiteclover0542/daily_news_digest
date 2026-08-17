# backend

FastAPI(Python) 기반 백엔드. 세 개의 하위 영역으로 나뉜다.

```
backend/
├── app/        # whiteclover 담당 — API 서버 (엔드포인트, 모델, 스키마, 비즈니스 로직)
├── pipeline/   # hoya 담당 — 뉴스 수집 → 전처리 → (ai 호출) → DB 적재, 스케줄러
├── ai/         # hoya 담당 — LLM 요약/카테고리 분류 로직
└── tests/      # 통합 테스트
```

## 아키텍처

```
[뉴스 수집 - RSS/API]        (pipeline/collectors)
        ↓
[전처리 - 정제, 중복제거, 필터링]  (pipeline/preprocessing)
        ↓
[LLM 요약 + 카테고리 분류]      (ai/)
        ↓
[DB 저장]                    (app/models)
        ↓
[백엔드 API]                  (app/api)
```

스케줄러(`pipeline/scheduler`)가 매일 새벽 자동 실행되어, `pipeline`이 수집·전처리를 하고 `ai`를 호출해 요약/분류 결과를 받아 DB에 적재하는 흐름을 돌린다.
