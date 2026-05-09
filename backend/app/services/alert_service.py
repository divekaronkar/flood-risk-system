from __future__ import annotations

import time

from sqlalchemy import select

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User


_LAST_ALERT_AT: dict[str, float] = {}


def send_broadcast_alerts(msg: str):
    """
    Actually sends the SMS/Email. This should be run in a background task.
    """
    db = SessionLocal()
    try:
        users = db.scalars(select(User)).all()
        
        # 1. SMS (Twilio)
        if (
            not settings.ALERT_SIMULATION_MODE
            and settings.TWILIO_ACCOUNT_SID
            and settings.TWILIO_AUTH_TOKEN
            and settings.TWILIO_FROM_NUMBER
        ):
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            for user in users:
                if user.phone_number:
                    try:
                        client.messages.create(
                            body=msg,
                            from_=settings.TWILIO_FROM_NUMBER,
                            to=user.phone_number,
                        )
                    except Exception as e:
                        print(f"Failed to send SMS to {user.phone_number}: {e}")

        # 2. Email (SMTP)
        if (
            not settings.ALERT_SIMULATION_MODE
            and settings.SMTP_HOST
            and settings.SMTP_USER
            and settings.SMTP_PASSWORD
        ):
            import smtplib
            from email.mime.text import MIMEText
            
            try:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    if settings.SMTP_TLS:
                        server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    
                    for user in users:
                        if user.email:
                            try:
                                email_msg = MIMEText(msg)
                                email_msg["Subject"] = "FLOOD RISK ALERT"
                                email_msg["From"] = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
                                email_msg["To"] = user.email
                                server.send_message(email_msg)
                            except Exception as e:
                                print(f"Failed to send email to {user.email}: {e}")
            except Exception as e:
                print(f"SMTP connection failed: {e}")

        # 3. Simulation Mode
        if settings.ALERT_SIMULATION_MODE:
            print(f"[ALERT SIMULATION] Broadcasting to {len(users)} users: {msg}")

    finally:
        db.close()


def maybe_send_alert(
    *, 
    risk_percent: float, 
    location_name: str | None = None, 
    force: bool = False,
    background_tasks = None
) -> tuple[bool, str | None]:
    if not force and risk_percent / 100.0 < settings.ALERT_RISK_THRESHOLD:
        return False, None

    msg = f"ALERT: Flood risk {risk_percent:.1f}%"
    if location_name:
        msg += f" at {location_name}"

    key = location_name or "__global__"
    now = time.time()
    last = _LAST_ALERT_AT.get(key, 0.0)
    if not force and (now - last < settings.ALERT_COOLDOWN_SECONDS):
        return False, None
    _LAST_ALERT_AT[key] = now

    if background_tasks:
        background_tasks.add_task(send_broadcast_alerts, msg)
    else:
        # Fallback to synchronous if no background_tasks provided (e.g. in scripts)
        send_broadcast_alerts(msg)

    return True, msg

