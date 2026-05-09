from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
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

    Base.metadata.create_all(bind=engine)

