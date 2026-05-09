import sys
from pathlib import Path

# Allow running as: `python backend/scripts/init_db.py`
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import init_db  # noqa: E402


def main() -> None:
    init_db()
    print("DB tables created/verified.")


if __name__ == "__main__":
    main()

