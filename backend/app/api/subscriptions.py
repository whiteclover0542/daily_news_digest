from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import crud
from app.schemas.subscription import PushSubscriptionIn, PushUnsubscribeIn

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("/push", status_code=204)
def subscribe_push(payload: PushSubscriptionIn, db: Session = Depends(get_db)) -> None:
    crud.subscribe_push(
        db, endpoint=payload.endpoint, p256dh=payload.keys.p256dh, auth=payload.keys.auth
    )
    db.commit()


@router.post("/push/unsubscribe", status_code=204)
def unsubscribe_push(payload: PushUnsubscribeIn, db: Session = Depends(get_db)) -> None:
    found = crud.unsubscribe_push(db, endpoint=payload.endpoint)
    db.commit()
    if not found:
        raise HTTPException(status_code=404, detail="Subscription not found")
