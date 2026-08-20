"""로컬 개발용 더미 데이터 시딩. 실행: python scripts/seed_dev_data.py (backend/ 에서, DATABASE_URL 설정 후)"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.models import crud  # noqa: E402

CATEGORIES = [
    ("정치", "politics"),
    ("경제", "economy"),
    ("IT", "it"),
    ("스포츠", "sports"),
    ("문화", "culture"),
]


def run() -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        categories = {
            slug: crud.get_or_create_category(db, name=name, slug=slug) for name, slug in CATEGORIES
        }

        now = datetime.now(timezone.utc)
        crud.upsert_article(
            db,
            title="기준금리 동결, 시장 반응은",
            source="테스트 경제신문",
            url="https://example.com/news/1",
            category=categories["economy"],
            summary="한국은행이 기준금리를 동결했다. 시장은 예상된 결정으로 받아들이는 분위기다.",
            published_at=now - timedelta(hours=2),
            keywords=["금리", "한국은행"],
        )
        crud.upsert_article(
            db,
            title="신규 AI 모델 공개",
            source="테스트 IT뉴스",
            url="https://example.com/news/2",
            category=categories["it"],
            summary="새로운 AI 모델이 공개되며 업계의 관심이 집중되고 있다.",
            published_at=now - timedelta(hours=1),
            keywords=["AI", "모델"],
        )
        db.commit()
        print("시드 데이터 생성 완료")
    finally:
        db.close()


if __name__ == "__main__":
    run()
