from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.history import HistoricalFloodRecord
from app.schemas.analytics import YearlyFloodTrend


router = APIRouter()


@router.get("/trends", response_model=list[YearlyFloodTrend])
def trends(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    current_year = datetime.now().year
    start_year = current_year - 9
    rows = db.scalars(
        select(HistoricalFloodRecord).where(HistoricalFloodRecord.year >= start_year).order_by(HistoricalFloodRecord.year)
    ).all()
    return [YearlyFloodTrend(year=r.year, flood_events=r.flood_events, avg_rainfall_mm=r.avg_rainfall_mm) for r in rows]

