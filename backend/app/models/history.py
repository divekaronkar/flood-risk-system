from sqlalchemy import Date, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HistoricalFloodRecord(Base):
    __tablename__ = "historical_flood_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    flood_events: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_rainfall_mm: Mapped[float] = mapped_column(Float, nullable=False)

