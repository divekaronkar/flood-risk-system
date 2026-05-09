from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    rainfall_mm: float = Field(..., ge=0)
    humidity: float = Field(..., ge=0, le=100)
    river_level_m: float = Field(..., ge=0)
    drainage_capacity: float = Field(..., ge=0, le=100)


class PredictResponse(BaseModel):
    risk_percent: float
    risk_level: str
    alert_triggered: bool
    alert_message: str | None = None

