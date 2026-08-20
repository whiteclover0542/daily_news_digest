import json
import logging

from pywebpush import WebPushException, webpush
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import PushSubscription

logger = logging.getLogger(__name__)


def send_push_to_all(db: Session, *, title: str, body: str, url: str = "/") -> None:
    """구독자 전원에게 푸시를 보낸다. 만료/삭제된 구독(404, 410)은 정리한다."""
    payload = json.dumps({"title": title, "body": body, "url": url})

    for subscription in db.query(PushSubscription).all():
        try:
            webpush(
                subscription_info={
                    "endpoint": subscription.endpoint,
                    "keys": {"p256dh": subscription.p256dh, "auth": subscription.auth},
                },
                data=payload,
                vapid_private_key=settings.vapid_private_key,
                vapid_claims={"sub": settings.vapid_subject},
            )
        except WebPushException as exc:
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code in (404, 410):
                db.delete(subscription)
            else:
                logger.warning("push failed for endpoint %s: %s", subscription.endpoint, exc)

    db.commit()
