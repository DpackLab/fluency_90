from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session as DBSession

from fluency90.models.user_streak import UserStreak

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True)
class UserDailyState:
    date: date
    active_today: bool
    has_output_today: bool
    blocked_without_output: bool
    current_streak: int
    session_active: bool
    session_started_at: Optional[datetime]
    derived_state: str


def _today_for_tz(user_tz: str) -> date:
    tz_key = (user_tz or "UTC").strip() or "UTC"
    try:
        tz = ZoneInfo(tz_key)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo("UTC")
    return datetime.now(tz).date()


def _day_bounds_utc(user_tz: str):
    """
    Retorna (start_utc, end_utc) del día 'hoy' según user_tz.
    Si el timezone es inválido, cae a UTC de forma gobernada.
    """
    tz_key = (user_tz or "UTC").strip() or "UTC"
    try:
        tz = ZoneInfo(tz_key)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo("UTC")

    now_local = datetime.now(tz)
    start_local = datetime(
        now_local.year,
        now_local.month,
        now_local.day,
        0, 0, 0,
        tzinfo=tz,
    )
    end_local = start_local + timedelta(days=1)

    start_utc = start_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_local.astimezone(ZoneInfo("UTC"))
    return start_utc, end_utc


def get_user_daily_state(db: DBSession, user_id: int, user_tz: str) -> UserDailyState:
    today = _today_for_tz(user_tz)
    start_utc, end_utc = _day_bounds_utc(user_tz)

    has_output_today = (
        db.execute(
            text("""
                SELECT 1
                FROM user_outputs
                WHERE user_id = :user_id
                  AND created_at >= :start_utc
                  AND created_at <  :end_utc
                LIMIT 1
            """),
            {"user_id": user_id, "start_utc": start_utc, "end_utc": end_utc},
        ).first()
        is not None
    )

    active_today = (
        db.execute(
            text("""
                SELECT 1
                FROM user_active_days
                WHERE user_id = :user_id
                  AND active_date = :today
                LIMIT 1
            """),
            {"user_id": user_id, "today": today},
        ).first()
        is not None
    )

    # Regla canónica: bloqueo solo si está activo hoy pero no produjo output hoy
    blocked_without_output = bool(active_today and (not has_output_today))

    streak_row = db.get(UserStreak, user_id)
    current_streak = streak_row.current_streak if streak_row else 0

    session_row = db.execute(
        text("""
            SELECT started_at
            FROM sessions
            WHERE user_id = :user_id
              AND ended_at IS NULL
            ORDER BY started_at DESC
            LIMIT 1
        """),
        {"user_id": user_id},
    ).first()

    session_active = session_row is not None
    session_started_at = session_row[0] if session_row else None

    # Estado derivado (útil para diagnóstico; no es "estado persistido")
    if active_today and has_output_today:
        derived_state = "ACTIVE_WITH_OUTPUT"
    elif active_today and (not has_output_today):
        derived_state = "ACTIVE_BLOCKED_NO_OUTPUT"
    else:
        derived_state = "INACTIVE_NO_OUTPUT"

    return UserDailyState(
        date=today,
        active_today=active_today,
        has_output_today=has_output_today,
        blocked_without_output=blocked_without_output,
        current_streak=current_streak,
        session_active=session_active,
        session_started_at=session_started_at,
        derived_state=derived_state,
    )
