from pydantic import BaseModel


class YearlyFloodTrend(BaseModel):
    year: int
    flood_events: int
    avg_rainfall_mm: float

