from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from app.core.config import settings
from app.db.session import SessionLocal
from app.ml.predict import predict_risk_percent, risk_level_from_percent
from app.models.location import RiskLocation
from app.services.alert_service import maybe_send_alert
from app.services.weather_service import fetch_open_meteo
from app.services.ws_manager import ws_manager


def _simulate_river_level(previous: float, rainfall_mm_1h: float) -> float:
    # Very simple dynamic: rainfall increases level, natural decay decreases it.
    lvl = float(previous) * 0.985 + float(rainfall_mm_1h) * 0.08
    return max(0.0, min(10.0, lvl))


async def _tick_once() -> None:
    db = SessionLocal()
    try:
        locations = db.scalars(select(RiskLocation)).all()
        changed = []
        for loc in locations:
            try:
                w = await fetch_open_meteo(loc.lat, loc.lng)
            except Exception:
                # If the API fails, skip updating this location this tick.
                continue

            loc.rainfall_mm = float(w.rainfall_mm_1h)
            loc.humidity = float(w.humidity_percent)
            loc.river_level_m = _simulate_river_level(loc.river_level_m, loc.rainfall_mm)

            risk = predict_risk_percent(loc.rainfall_mm, loc.humidity, loc.river_level_m, loc.drainage_capacity)
            loc.risk_percent = risk
            loc.risk_level = risk_level_from_percent(risk)

            db.add(loc)
            maybe_send_alert(risk_percent=risk, location_name=loc.name)
            changed.append(
                {
                    "id": loc.id,
                    "name": loc.name,
                    "lat": loc.lat,
                    "lng": loc.lng,
                    "rainfall_mm": loc.rainfall_mm,
                    "humidity": loc.humidity,
                    "river_level_m": loc.river_level_m,
                    "drainage_capacity": loc.drainage_capacity,
                    "risk_percent": loc.risk_percent,
                    "risk_level": loc.risk_level,
                    "is_dam": bool(loc.is_dam),
                }
            )

        db.commit()
        if changed:
            await ws_manager.broadcast_json(
                {"type": "locations_update", "at": datetime.now(timezone.utc).isoformat(), "locations": changed}
            )
    finally:
        db.close()


async def realtime_loop() -> None:
    """
    Background loop started by FastAPI.
    Updates rainfall/humidity from Open-Meteo and recomputes risks.
    """
    if not settings.REALTIME_ENABLED:
        return

    while True:
        try:
            await _tick_once()
        except Exception as e:
            print(f"Realtime tick failed: {e}")

        await asyncio.sleep(max(10, int(settings.REALTIME_REFRESH_SECONDS)))

