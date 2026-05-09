from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.location import RiskLocation


router = APIRouter()


@router.get("")
def stats(db: Session = Depends(get_db), _user=Depends(get_current_user)) -> dict:
    total = db.scalar(select(func.count()).select_from(RiskLocation)) or 0
    high = db.scalar(select(func.count()).select_from(RiskLocation).where(RiskLocation.risk_level == "High")) or 0
    medium = (
        db.scalar(select(func.count()).select_from(RiskLocation).where(RiskLocation.risk_level == "Medium")) or 0
    )
    low = db.scalar(select(func.count()).select_from(RiskLocation).where(RiskLocation.risk_level == "Low")) or 0

    avg_risk = db.scalar(select(func.avg(RiskLocation.risk_percent))) or 0.0

    return {
        "total_locations": int(total),
        "high": int(high),
        "medium": int(medium),
        "low": int(low),
        "avg_risk_percent": float(avg_risk),
    }

