from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base


engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    connect_args={"connect_timeout": 10}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    # Import models so SQLAlchemy knows them.
    from app.models.user import User  # noqa: F401
    from app.models.location import RiskLocation  # noqa: F401
    from app.models.history import HistoricalFloodRecord  # noqa: F401

    import time
    from sqlalchemy import text
    max_retries = 5
    for i in range(max_retries):
        try:
            # Create tables
            Base.metadata.create_all(bind=engine)
            return
        except Exception as e:
            if i == max_retries - 1:
                raise e
            print(f"⚠️ DB connection failed (attempt {i+1}/{max_retries}). Retrying in 5s...")
            time.sleep(5)

