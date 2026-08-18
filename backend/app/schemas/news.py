from datetime import datetime

from pydantic import BaseModel

from app.schemas.category import CategoryOut


class NewsListItem(BaseModel):
    id: int
    title: str
    source: str
    category: CategoryOut
    summary_preview: str
    published_at: datetime


class NewsListResponse(BaseModel):
    date: str
    total: int
    page: int
    limit: int
    items: list[NewsListItem]


class NewsDetail(BaseModel):
    id: int
    title: str
    source: str
    url: str
    category: CategoryOut
    summary: str
    keywords: list[str]
    published_at: datetime
    collected_at: datetime
