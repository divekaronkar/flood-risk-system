from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class WeatherSnapshot:
    rainfall_mm_1h: float
    humidity_percent: float


async def fetch_open_meteo(lat: float, lng: float) -> WeatherSnapshot:
    """
    Uses Open-Meteo forecast API (no key required).
    We fetch:
    - precipitation (last hour proxy)
    - relative humidity
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": "relative_humidity_2m,precipitation",
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()

    current = data.get("current") or {}
    humidity = float(current.get("relative_humidity_2m") or 0.0)
    precipitation = float(current.get("precipitation") or 0.0)
    return WeatherSnapshot(rainfall_mm_1h=precipitation, humidity_percent=humidity)

