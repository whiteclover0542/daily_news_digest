"""수동 푸시 발송 트리거. 스케줄러가 붙기 전까지 로컬/CLI에서 테스트·발송용으로 사용.
실행: python scripts/send_push.py "제목" "본문" [url] (backend/ 에서, 환경변수 설정 후)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal  # noqa: E402
from app.services.push import send_push_to_all  # noqa: E402


def run() -> None:
    if len(sys.argv) < 3:
        print('사용법: python scripts/send_push.py "제목" "본문" [url]')
        sys.exit(1)

    title, body = sys.argv[1], sys.argv[2]
    url = sys.argv[3] if len(sys.argv) > 3 else "/"

    db = SessionLocal()
    try:
        send_push_to_all(db, title=title, body=body, url=url)
        print("발송 완료")
    finally:
        db.close()


if __name__ == "__main__":
    run()
