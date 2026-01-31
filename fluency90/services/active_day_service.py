from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DBSession

from fluency90.models.user_active_day import UserActiveDay
from fluency90.services.streak_service import update_user_streak

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def _today_for_tz(user_tz: str) -> date:
    tz_key = (user_tz or "UTC").strip() or "UTC"
    try:
        tz = ZoneInfo(tz_key)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo("UTC")
    return datetime.now(tz).date()

def mark_user_active_today(db: DBSession, user_id: int, user_tz: str) -> None:
    """
    Marca el día activo del usuario según SU timezone (IANA).
    Idempotente por UNIQUE(user_id, active_date).
    """
    today = _today_for_tz(user_tz)

    record = UserActiveDay(
        user_id=user_id,
        active_date=today,
        created_at=datetime.now(timezone.utc),
    )
    db.add(record)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # ya estaba marcado; esto es esperado
        update_user_streak(db, user_id, user_tz)
        return

    update_user_streak(db, user_id, user_tz)
