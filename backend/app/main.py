from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import init_db
from app.services.realtime_service import realtime_loop


app = FastAPI(title="Flood-Risk Detection System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    print("🚀 Starting application startup sequence...")
    try:
        # Check DB connection
        from sqlalchemy import text
        from app.db.session import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection verified.")

        init_db()
        print("✅ Database tables initialized.")

        # Auto-seed if empty
        from sqlalchemy import select
        from app.db.session import SessionLocal
        from app.models.location import RiskLocation
        db = SessionLocal()
        try:
            exists = db.scalar(select(RiskLocation).limit(1))
            if not exists:
                print("📝 Database empty. Auto-seeding initial data...")
                from scripts.seed_data import seed_locations, seed_history
                seed_locations()
                seed_history()
                print("✅ Auto-seeding complete.")
            else:
                print("ℹ️ Database already contains data. Skipping seeding.")
        finally:
            db.close()
    except Exception as e:
        print(f"❌ ERROR during startup: {e}")

    # Pre-load ML model to avoid lag on first prediction
    from app.ml.predict import _load_model
    try:
        _load_model()
        print("ML Model loaded successfully.")
    except Exception as e:
        print(f"ML Model load failed: {e}")

    # Start realtime updater in background
    import asyncio

    asyncio.create_task(realtime_loop())


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api")

