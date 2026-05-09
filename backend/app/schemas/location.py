from pydantic import BaseModel


class RiskLocationOut(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    rainfall_mm: float
    humidity: float
    river_level_m: float
    drainage_capacity: float
    risk_percent: float
    risk_level: str
    is_dam: bool


class AdminUpdateLocationRequest(BaseModel):
    rainfall_mm: float | None = None
    humidity: float | None = None
    river_level_m: float | None = None
    drainage_capacity: float | None = None

