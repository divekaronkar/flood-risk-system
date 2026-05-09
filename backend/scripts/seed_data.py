from datetime import datetime

import sys
from pathlib import Path

from sqlalchemy import select

# Allow running as: `python backend/scripts/seed_data.py`
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal, init_db
from app.models.history import HistoricalFloodRecord
from app.models.location import RiskLocation
from app.ml.predict import predict_risk_percent, risk_level_from_percent


def seed_locations() -> None:
    db = SessionLocal()
    try:
        # Clear existing to ensure fresh start with Pune/India data
        db.query(RiskLocation).delete()
        db.commit()

        # Expanded list: Pune rivers/dams and major Indian rivers/dams.
        # Format: (name, lat, lng, is_dam)
        points = [
            # --- PUNE ---
            ("Mula River (Pune)", 18.5538, 73.8125, False),
            ("Mutha River (Pune)", 18.5204, 73.8567, False),
            ("Khadakwasla Dam (Pune)", 18.4372, 73.7634, True),
            ("Panshet Dam (Pune)", 18.3980, 73.6140, True),
            ("Varasgaon Dam (Pune)", 18.4110, 73.6020, True),
            ("Temghar Dam (Pune)", 18.4550, 73.5420, True),
            ("Pavana Dam (Lonavala/Pune)", 18.6600, 73.4800, True),
            ("Mulshi Dam (Pune)", 18.4870, 73.4750, True),
            
            # --- INDIA RIVERS ---
            ("Ganga (Varanasi)", 25.3176, 83.0062, False),
            ("Yamuna (Delhi)", 28.6139, 77.2090, False),
            ("Brahmaputra (Guwahati)", 26.1445, 91.7362, False),
            ("Narmada (Jabalpur)", 23.1815, 79.9864, False),
            ("Godavari (Rajahmundry)", 17.0005, 81.7729, False),
            ("Krishna (Vijayawada)", 16.5062, 80.6480, False),
            ("Kaveri (Tiruchirappalli)", 10.8505, 78.6850, False),
            ("Mahanadi (Cuttack)", 20.4625, 85.8830, False),
            ("Tapi (Surat)", 21.1702, 72.8311, False),
            ("Sabarmati (Ahmedabad)", 23.0225, 72.5714, False),
            ("Hooghly (Kolkata)", 22.5726, 88.3639, False),
            ("Indus (Leh)", 34.1526, 77.5771, False),

            # --- INDIA DAMS ---
            ("Tehri Dam (Uttarakhand)", 30.3770, 78.4800, True),
            ("Bhakra Dam (Himachal)", 31.4100, 76.4300, True),
            ("Sardar Sarovar (Gujarat)", 21.8300, 73.7500, True),
            ("Hirakud Dam (Odisha)", 21.5700, 83.8700, True),
            ("Nagarjuna Sagar (Telangana)", 16.5700, 79.3100, True),
            ("Idukki Dam (Kerala)", 9.8500, 76.9700, True),
            ("Koyna Dam (Maharashtra)", 17.4000, 73.7400, True),
            ("Mettur Dam (Tamil Nadu)", 11.7900, 77.8000, True),
            ("Tungabhadra Dam (Karnataka)", 15.2600, 76.3400, True),
            ("Rihand Dam (UP)", 24.2100, 83.0300, True),
        ]

        for name, lat, lng, is_dam in points:
            rainfall_mm = 10.0
            humidity = 60.0
            river_level_m = 2.0
            drainage_capacity = 70.0

            risk_percent = predict_risk_percent(rainfall_mm, humidity, river_level_m, drainage_capacity)
            loc = RiskLocation(
                name=name,
                lat=lat,
                lng=lng,
                rainfall_mm=rainfall_mm,
                humidity=humidity,
                river_level_m=river_level_m,
                drainage_capacity=drainage_capacity,
                risk_percent=risk_percent,
                risk_level=risk_level_from_percent(risk_percent),
                is_dam=int(is_dam),
            )
            db.add(loc)

        db.commit()
    finally:
        db.close()


def seed_history() -> None:
    db = SessionLocal()
    try:
        existing = db.scalar(select(HistoricalFloodRecord).limit(1))
        if existing:
            return

        current_year = datetime.now().year
        for y in range(current_year - 9, current_year + 1):
            # Simulated yearly trend.
            flood_events = int(2 + (y - (current_year - 9)) * 0.4)  # gentle upward trend
            avg_rainfall_mm = float(850 + (y - (current_year - 9)) * 12)
            db.add(HistoricalFloodRecord(year=y, flood_events=flood_events, avg_rainfall_mm=avg_rainfall_mm))
        db.commit()
    finally:
        db.close()


def main() -> None:
    init_db()
    seed_locations()
    seed_history()
    print("Seed completed.")


if __name__ == "__main__":
    main()

