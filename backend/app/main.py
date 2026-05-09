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
    # If MySQL isn't running yet, we still want the API to start
    # (frontend can be developed independently). When DB becomes available,
    # restart the API to create tables.
    try:
        init_db()
    except Exception as e:
        print(f"DB init skipped (startup): {e}")

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

