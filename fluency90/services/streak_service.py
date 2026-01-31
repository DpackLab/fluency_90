from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session as DBSession

from fluency90.models.user_streak import UserStreak

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def _today_for_tz(user_tz: str) -> date:
    tz_key = (user_tz or "UTC").strip() or "UTC"
    try:
        tz = ZoneInfo(tz_key)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo("UTC")
    return datetime.now(tz).date()

def update_user_streak(db: DBSession, user_id: int, user_tz: str) -> None:
    today = _today_for_tz(user_tz)

    streak = db.get(UserStreak, user_id)

    # Caso 1: primera vez (no existe fila)
    if streak is None:
        streak = UserStreak(
            user_id=user_id,
            current_streak=1,
            last_active_date=today,
            updated_at=datetime.now(timezone.utc),
        )
        db.add(streak)
        db.commit()
        return

    # Caso 2: ya se contó hoy (idempotente)
    if streak.last_active_date == today:
        return

    # Caso 3: venía activo ayer -> incrementa
    if streak.last_active_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        # Caso 4: se rompió la cadena -> reinicia
        streak.current_streak = 1

    streak.last_active_date = today
    streak.updated_at = datetime.now(timezone.utc)
    db.commit()
