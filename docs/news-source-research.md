# 뉴스 소스 조사 및 MVP 결정

조사일: 2026-09-03

## 최종 결정

MVP 뉴스 소스는 **과학기술정보통신부 보도자료**로 정한다. 초기 데이터 범위는 IT이며, RSS에서 새 보도자료 목록을 확인한 뒤 상세 페이지와 공개 첨부 PDF/HWPX에서 전문을 수집한다.

과기정통부 보도자료는 공공누리 제1유형(출처표시)으로 제공되며, 확인한 자료에는 AI 학습 가능 표시도 있다. 따라서 원문 출처를 명시하고, 원문에 있는 사실만 짧게 요약해 제공한다.

## 후보 비교

| 후보 | 다루는 범위 | 전문 수집 방식 | 이용 근거 | MVP 판단 |
|---|---|---|---|---|
| 과학기술정보통신부 | AI, 반도체, 통신, 디지털 정책, 연구개발 | 보도자료 RSS → 상세 페이지·첨부 PDF/HWPX | 공공누리 제1유형, AI 학습 가능 표시 확인 | **선정** |
| 행정안전부 | 재난, 공공서비스, 지방행정, 제도 | RSS → 상세 페이지·첨부 자료 | 공공누리 제1유형 | 2차 확장 후보 |
| 문화체육관광부 | 문화, 관광, 콘텐츠, 체육 정책 | RSS → 상세 페이지·첨부 자료 | 공공누리 제1유형 | 2차 확장 후보 |
| 산업통상자원부 | 산업, 통상, 에너지, 수출 | RSS → 상세 페이지·첨부 자료 | 공공누리 제1유형 | 2차 확장 후보 |

일반 언론사 RSS는 무료여도 개인 비상업적 이용으로 제한하거나, 전문 수집·AI 요약·서비스 재게시 허용 범위가 불명확한 경우가 있어 MVP 소스로 사용하지 않는다.

## 수집·요약 흐름

```text
과기정통부 보도자료 RSS에서 새 항목 확인
        ↓
상세 페이지 및 공개 첨부 PDF/HWPX 전문 수집
        ↓
본문 정제·중복 URL 제거
        ↓
핵심 결정·수치·일정·대상·영향을 4~6문장으로 요약
        ↓
IT 카테고리로 DB 적재 후 원문 링크와 함께 표시
```

## 갱신 일정

- KST 오전 6시: 전날 이후 새 자료 수집·요약 → 오전 7시 브리핑 준비
- KST 오후 1시: 당일 게시 자료 보강 수집
- 스케줄러는 Render 무료 서비스의 슬립 영향을 피하기 위해 GitHub Actions cron을 사용한다.

## 공통 수집 형식

```python
CollectedArticle = {
    "title": str,
    "source": "과학기술정보통신부",
    "url": str,
    "published_at": datetime,
    "content": str,
    "source_category": "IT",
}
```

- URL은 정규화한 뒤 기존 `upsert_article()`의 중복 방지 키로 사용한다.
- 요약에는 원문에 없는 배경·전망을 넣지 않는다.
- 화면에는 출처와 원문 링크를 함께 표시한다.

## 공식 근거

- [과기정통부 RSS 이용 안내](https://www.msit.go.kr/contents/cont.do?mId=173&mPid=147&sCode=user)
- [과기정통부 보도자료 및 공공누리·AI 학습 가능 표시 사례](https://www.msit.go.kr/bbs/view.do?bbsSeqNo=94&mId=307&mPid=208&nttSeqNo=3187237&sCode=user)
- [행정안전부 보도자료 공공누리 제1유형 사례](https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardArticle.do?bbsId=BBSMSTR_000000000008&nttId=121195)
- [문화체육관광부 RSS·공공누리 안내](https://www.mcst.go.kr/site/s_etc/rss/rssService.jsp)
- [산업통상자원부 보도자료 공공누리 제1유형 안내](https://motie.go.kr/kor/article/ATCL3f49a5a8c?pageIndex=8)
