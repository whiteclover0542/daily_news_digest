# ai

LLM 기반 요약/카테고리 분류 로직. `pipeline`이 기사를 수집·전처리한 뒤 이 모듈을 호출해 요약문과 카테고리를 얻고, 그 결과를 DB에 적재한다.

```
ai/
├── client.py      # LLM API 클라이언트 래퍼
├── summarize.py   # 기사 요약
├── classify.py    # 카테고리 분류
└── prompts/       # 프롬프트 템플릿
```

`app`(API 서버)과 달리 상시 서비스가 아니라, 파이프라인 실행 시점에 호출되는 모듈이다.
