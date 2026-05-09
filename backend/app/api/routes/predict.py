from fastapi import APIRouter, Depends, BackgroundTasks

from app.api.deps import get_current_user
from app.ml.predict import predict_risk_percent, risk_level_from_percent
from app.schemas.prediction import PredictRequest, PredictResponse
from app.services.alert_service import maybe_send_alert


router = APIRouter()


@router.post("", response_model=PredictResponse)
def predict(
    payload: PredictRequest, 
    background_tasks: BackgroundTasks,
    _user=Depends(get_current_user)
) -> PredictResponse:
    risk_percent = predict_risk_percent(
        payload.rainfall_mm, payload.humidity, payload.river_level_m, payload.drainage_capacity
    )
    level = risk_level_from_percent(risk_percent)
    triggered, msg = maybe_send_alert(risk_percent=risk_percent, background_tasks=background_tasks)
    return PredictResponse(
        risk_percent=risk_percent,
        risk_level=level,
        alert_triggered=triggered,
        alert_message=msg,
    )

