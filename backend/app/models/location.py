from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RiskLocation(Base):
    """
    Represents a point on the map with the latest observed/simulated features.
    Admin can update river_level/drainage_capacity to see risk update.
    """

    __tablename__ = "risk_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)

    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    humidity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    river_level_m: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    drainage_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    risk_percent: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False, default="Low")

    is_dam: Mapped[bool] = mapped_column(Integer, nullable=False, default=0)  # Use Integer (0/1) for SQLite/MySQL compat

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

