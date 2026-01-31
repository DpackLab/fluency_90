from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.orm import Session

from fluency90.models.user_output import UserOutput


def _safe_tz(user_tz: str) -> ZoneInfo:
    tz_key = (user_tz or "UTC").strip() or "UTC"
    try:
        return ZoneInfo(tz_key)
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def get_output_today_metrics(db: Session, user_id: int, user_tz: str) -> dict:
    """
    Deriva métricas de output del día (según timezone del usuario), SIN writes.
    Retorna: {has_output_today, outputs_today_count, first_output_at, last_output_at}
    """
    tz = _safe_tz(user_tz)

    now_local = datetime.now(tz)
    start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = start_local.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Convertimos a UTC para filtrar en created_at (timestamptz)
    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)

    q = (
        db.query(UserOutput.created_at)
        .filter(UserOutput.user_id == user_id)
        .filter(UserOutput.created_at >= start_utc)
        .filter(UserOutput.created_at <= end_utc)
        .order_by(UserOutput.created_at.asc())
    )

    rows = q.all()
    if not rows:
        return {
            "has_output_today": False,
            "outputs_today_count": 0,
            "first_output_at": None,
            "last_output_at": None,
        }

    first = rows[0][0]
    last = rows[-1][0]
    return {
        "has_output_today": True,
        "outputs_today_count": len(rows),
        "first_output_at": first,
        "last_output_at": last,
    }
