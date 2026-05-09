from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.ml.predict import predict_risk_percent, risk_level_from_percent
from app.models.location import RiskLocation
from app.schemas.location import AdminUpdateLocationRequest, RiskLocationOut
from app.services.alert_service import maybe_send_alert


router = APIRouter()


@router.get("", response_model=list[RiskLocationOut])
def list_locations(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    items = db.scalars(select(RiskLocation).order_by(RiskLocation.id)).all()
    return [
        RiskLocationOut(
            id=i.id,
            name=i.name,
            lat=i.lat,
            lng=i.lng,
            rainfall_mm=i.rainfall_mm,
            humidity=i.humidity,
            river_level_m=i.river_level_m,
            drainage_capacity=i.drainage_capacity,
            risk_percent=i.risk_percent,
            risk_level=i.risk_level,
            is_dam=bool(i.is_dam),
        )
        for i in items
    ]


@router.post("/broadcast-alert")
def broadcast_manual_alert(
    payload: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    msg = payload.get("message")
    if not msg:
        raise HTTPException(status_code=400, detail="Message is required")

    from app.services.alert_service import maybe_send_alert
    # We force an alert by passing a high risk_percent and force=True.
    maybe_send_alert(risk_percent=100.0, location_name=f"MANUAL: {msg}", force=True, background_tasks=background_tasks)
    return {"status": "Alert broadcasted"}


@router.patch("/{location_id}", response_model=RiskLocationOut)
def admin_update_location(
    location_id: int,
    payload: AdminUpdateLocationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    loc = db.scalar(select(RiskLocation).where(RiskLocation.id == location_id))
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")

    for field in ["rainfall_mm", "humidity", "river_level_m", "drainage_capacity"]:
        value = getattr(payload, field)
        if value is not None:
            setattr(loc, field, float(value))

    # Recompute risk using the ML model.
    risk_percent = predict_risk_percent(loc.rainfall_mm, loc.humidity, loc.river_level_m, loc.drainage_capacity)
    loc.risk_percent = risk_percent
    loc.risk_level = risk_level_from_percent(risk_percent)

    db.add(loc)
    db.commit()
    db.refresh(loc)

    maybe_send_alert(risk_percent=risk_percent, location_name=loc.name, background_tasks=background_tasks)

    return RiskLocationOut(
        id=loc.id,
        name=loc.name,
        lat=loc.lat,
        lng=loc.lng,
        rainfall_mm=loc.rainfall_mm,
        humidity=loc.humidity,
        river_level_m=loc.river_level_m,
        drainage_capacity=loc.drainage_capacity,
        risk_percent=loc.risk_percent,
        risk_level=loc.risk_level,
        is_dam=bool(loc.is_dam),
    )

