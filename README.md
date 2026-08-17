# daily_news_digest

매일 아침, 그날의 뉴스를 자동으로 수집·요약·분류해서 보여주는 PWA 앱 (2인 개인 포트폴리오 프로젝트)

- 프로젝트 기획: [프로젝트기획서.md](./docs/프로젝트기획서.md)
- 진행 로그: [docs/progress/](./docs/progress/README.md)
- API 명세: [docs/api-spec.md](./docs/api-spec.md)
- DB 스키마: [docs/db-schema.md](./docs/db-schema.md)

## 폴더 구조

```
daily_news_digest/
├── backend/
│   ├── app/            # FastAPI 서버 (API, 모델, 스키마, 서비스)
│   ├── pipeline/        # 뉴스 수집 → 전처리 → DB 적재, 스케줄러
│   ├── ai/              # LLM 요약/카테고리 분류
│   └── tests/
├── frontend/            # React/Next.js 기반 PWA
└── docs/                # 기획, API 명세, DB 스키마, 주간 진행 로그
```

## 역할 분담

| 담당 | 작업 | 관련 폴더 |
|---|---|---|
| hoya — 데이터/AI 파이프라인 | 뉴스 수집, 전처리, 스케줄러, LLM 요약·분류, DB 적재 | `backend/pipeline/`, `backend/ai/` |
| whiteclover — 백엔드/프론트/인프라 | API 서버, 프론트(PWA), 알림 기능, 배포 | `backend/app/`, `frontend/` |

자세한 내용은 [프로젝트기획서.md](./docs/프로젝트기획서.md) 참고.
