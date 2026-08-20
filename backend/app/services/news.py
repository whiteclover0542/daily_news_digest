from datetime import date as date_type
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Article, Category
from app.schemas.category import CategoryOut
from app.schemas.news import NewsDetail, NewsListItem, NewsListResponse

SUMMARY_PREVIEW_LENGTH = 80
KST = ZoneInfo("Asia/Seoul")


def today_kst() -> date_type:
    return datetime.now(KST).date()


def _kst_day_range_utc(target_date: date_type) -> tuple[datetime, datetime]:
    """KST 기준 target_date 하루(00:00~24:00)에 해당하는 UTC 구간을 반환한다.

    SQLite의 DateTime 타입은 tz-aware 값을 실제로 UTC 변환하지 않고 시각 숫자를
    그대로 저장하므로(DB에 저장된 published_at은 항상 UTC 시각), 쿼리 바인딩
    전에 반드시 UTC로 변환해서 넘겨야 한다.
    """
    start_kst = datetime.combine(target_date, time.min, tzinfo=KST)
    end_kst = start_kst + timedelta(days=1)
    return start_kst.astimezone(timezone.utc), end_kst.astimezone(timezone.utc)


def _category_out(category: Category) -> CategoryOut:
    return CategoryOut(id=category.id, name=category.name, slug=category.slug)


def _to_list_item(article: Article) -> NewsListItem:
    return NewsListItem(
        id=article.id,
        title=article.title,
        source=article.source,
        category=_category_out(article.category),
        summary_preview=article.summary[:SUMMARY_PREVIEW_LENGTH],
        published_at=article.published_at,
    )


def to_detail(article: Article) -> NewsDetail:
    return NewsDetail(
        id=article.id,
        title=article.title,
        source=article.source,
        url=article.url,
        category=_category_out(article.category),
        summary=article.summary,
        keywords=[keyword.word for keyword in article.keywords],
        published_at=article.published_at,
        collected_at=article.collected_at,
    )


def list_news(
    db: Session,
    *,
    target_date: date_type,
    category_slug: str | None,
    page: int,
    limit: int,
) -> NewsListResponse:
    range_start, range_end = _kst_day_range_utc(target_date)
    base_query = (
        select(Article)
        .join(Article.category)
        .where(Article.published_at >= range_start, Article.published_at < range_end)
    )
    if category_slug:
        base_query = base_query.where(Category.slug == category_slug)

    total = db.scalar(select(func.count()).select_from(base_query.subquery())) or 0

    items_query = (
        base_query.options(selectinload(Article.category))
        .order_by(Article.published_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    articles = db.scalars(items_query).all()

    return NewsListResponse(
        date=target_date.isoformat(),
        total=total,
        page=page,
        limit=limit,
        items=[_to_list_item(article) for article in articles],
    )


def get_article(db: Session, article_id: int) -> Article | None:
    return db.get(
        Article,
        article_id,
        options=[selectinload(Article.category), selectinload(Article.keywords)],
    )
