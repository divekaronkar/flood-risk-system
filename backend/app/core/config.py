from pathlib import Path

import json

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _pick_env_file() -> str:
    """
    We run uvicorn from the repo root with `--app-dir backend`,
    so `.env` usually lives at `backend/.env` (not repo-root `.env`).
    """
    repo_root = Path(__file__).resolve().parents[3]
    backend_env = repo_root / "backend" / ".env"
    root_env = repo_root / ".env"
    if backend_env.exists():
        return str(backend_env)
    return str(root_env)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_pick_env_file(), extra="ignore")

    APP_ENV: str = "dev"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # MySQL: mysql+pymysql://USER:PASSWORD@HOST:3306/DBNAME
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/flood_risk"

    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # ML model path
    MODEL_PATH: str = str(Path(__file__).resolve().parents[1] / "ml" / "model.joblib")

    # Simulated SMS settings
    ALERT_RISK_THRESHOLD: float = 0.80
    ALERT_SIMULATION_MODE: bool = True
    ALERT_COOLDOWN_SECONDS: int = 300

    # Twilio (optional)
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_FROM_NUMBER: str | None = None
    TWILIO_TO_NUMBER: str | None = None

    # SMTP / Email (optional)
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str | None = None
    SMTP_TLS: bool = True

    # Real-time refresh (Open-Meteo)
    REALTIME_ENABLED: bool = True
    REALTIME_REFRESH_SECONDS: int = 60

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _fix_database_url(cls, v: str) -> str:
        if v.startswith("mysql://"):
            return v.replace("mysql://", "mysql+pymysql://", 1)
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v):
        # Support env formats like:
        # CORS_ORIGINS=["http://localhost:5173"]  (JSON)
        # CORS_ORIGINS=http://localhost:5173     (single string)
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                try:
                    parsed = json.loads(s)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
            return [s]
        return ["http://localhost:5173", "http://127.0.0.1:5173"]


settings = Settings()

