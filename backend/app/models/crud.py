from datetime import datetime

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.category import Category
from app.models.keyword import Keyword
from app.models.push_subscription import PushSubscription


def get_or_create_category(db: Session, *, name: str, slug: str) -> Category:
    category = db.query(Category).filter_by(slug=slug).one_or_none()
    if category is None:
        category = Category(name=name, slug=slug)
        db.add(category)
        db.flush()
    return category


def get_or_create_keyword(db: Session, word: str) -> Keyword:
    keyword = db.query(Keyword).filter_by(word=word).one_or_none()
    if keyword is None:
        keyword = Keyword(word=word)
        db.add(keyword)
        db.flush()
    return keyword


def upsert_article(
    db: Session,
    *,
    title: str,
    source: str,
    url: str,
    category: Category,
    summary: str,
    published_at: datetime,
    keywords: list[str] | None = None,
) -> Article:
    """url이 이미 수집된 기사면 기존 레코드를 그대로 반환해 중복 적재를 막는다."""
    article = db.query(Article).filter_by(url=url).one_or_none()
    if article is not None:
        return article

    article = Article(
        title=title,
        source=source,
        url=url,
        category=category,
        summary=summary,
        published_at=published_at,
    )
    db.add(article)
    if keywords:
        article.keywords = [get_or_create_keyword(db, word) for word in keywords]

    db.flush()
    return article


def subscribe_push(db: Session, *, endpoint: str, p256dh: str, auth: str) -> PushSubscription:
    """endpoint가 이미 구독돼 있으면 키만 갱신해 재구독을 멱등하게 처리한다."""
    subscription = db.query(PushSubscription).filter_by(endpoint=endpoint).one_or_none()
    if subscription is None:
        subscription = PushSubscription(endpoint=endpoint, p256dh=p256dh, auth=auth)
        db.add(subscription)
    else:
        subscription.p256dh = p256dh
        subscription.auth = auth
    db.flush()
    return subscription


def unsubscribe_push(db: Session, *, endpoint: str) -> bool:
    subscription = db.query(PushSubscription).filter_by(endpoint=endpoint).one_or_none()
    if subscription is None:
        return False
    db.delete(subscription)
    db.flush()
    return True
