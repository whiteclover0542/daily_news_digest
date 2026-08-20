from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.news import NewsDetail, NewsListResponse
from app.services import news as news_service

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=NewsListResponse)
def get_news_list(
    category: str | None = Query(default=None, description="카테고리 slug"),
    date: date_type | None = Query(default=None, description="YYYY-MM-DD, 기본값 오늘(KST)"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
) -> NewsListResponse:
    target_date = date or news_service.today_kst()
    return news_service.list_news(
        db, target_date=target_date, category_slug=category, page=page, limit=limit
    )


@router.get("/{article_id}", response_model=NewsDetail)
def get_news_detail(article_id: int, db: Session = Depends(get_db)) -> NewsDetail:
    article = news_service.get_article(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return news_service.to_detail(article)
