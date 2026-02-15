from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy import text
from sqlalchemy.orm import Session as DBSession


@dataclass(frozen=True)
class ProgressDecision:
    allowed: bool
    reason: str | None = None
    has_output_today: bool = False
    today: str | None = None  # ISO date (debug-friendly)
    signals_used: list[str] | None = None


def _safe_tz(user_tz: str | None) -> ZoneInfo:
    tz_key = (user_tz or "UTC").strip() or "UTC"
    try:
        return ZoneInfo(tz_key)
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def _today_for_tz(user_tz: str | None) -> str:
    tz = _safe_tz(user_tz)
    return datetime.now(tz).date().isoformat()


def has_output_today(db: DBSession, user_id: int, user_tz: str | None) -> bool:
    """
    Regla: NO usamos AT TIME ZONE en SQL para evitar fallos por tz inválida.
    Convertimos tz en Python de forma segura y comparamos contra rango UTC.
    """
    tz = _safe_tz(user_tz)
    now_local = datetime.now(tz)
    start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = start_local + timedelta(days=1)  # fin exclusivo

    start_utc = start_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_local.astimezone(ZoneInfo("UTC"))

    row = db.execute(
        text(
            """
            SELECT 1
            FROM user_outputs
            WHERE user_id = :user_id
              AND created_at >= :start_utc
              AND created_at < :end_utc
            LIMIT 1
            """
        ),
        {"user_id": user_id, "start_utc": start_utc, "end_utc": end_utc},
    ).first()

    return row is not None

def evaluate_progress_state(
    db: DBSession,
    user_id: int,
    user_tz: str | None,
    *,
    active_today: bool,
    blocked_without_output: bool,
    endpoint_path: str | None = None,
    request_id: str | None = None,
    has_output_today_override: bool | None = None,
    today_override: str | None = None,
) -> ProgressDecision:

    """
    Política canónica (Semana 7 Día 3):
    - Compatibilidad / verdad mínima: si blocked_without_output=True, bloquear.
    - Regla real: bloquear si active_today=True y no hay output hoy.
    - En cualquier otro caso, permitir.
    """

    today = today_override or _today_for_tz(user_tz)
    has_out = has_output_today_override if has_output_today_override is not None else has_output_today(
        db=db, user_id=user_id, user_tz=user_tz
    )

    if blocked_without_output:
        decision = ProgressDecision(
            allowed=False,
            reason="Output requerido para continuar",
            has_output_today=has_out,
            today=today,
            signals_used=["daily_state.blocked_without_output"],
        )
    elif active_today and (not has_out):
        decision = ProgressDecision(
            allowed=False,
            reason="Output requerido para continuar",
            has_output_today=False,
            today=today,
            signals_used=["active_today", "has_output_today"],
        )
    else:
        decision = ProgressDecision(
            allowed=True,
            reason=None,
            has_output_today=has_out,
            today=today,
            signals_used=["allow"],
        )

    return decision

def decision_from_state(
    db: DBSession,
    *,
    user_id: int,
    user_tz: str | None,
    state,
    endpoint_path: str | None = None,
    request_id: str | None = None,
) -> ProgressDecision:
    """
    Semana 8 Día 2 — Adaptador único (daily_state -> ProgressDecision)
    Regla: el endpoint NO interpreta flags; solo pasa state.
    """
    # state viene de get_user_daily_state (UserDailyState)
    today_iso = getattr(getattr(state, "date", None), "isoformat", lambda: None)()
    has_out = bool(getattr(state, "has_output_today", False))
    active_today = bool(getattr(state, "active_today", False))
    blocked_without_output = bool(getattr(state, "blocked_without_output", False))

    return evaluate_progress_state(
        db=db,
        user_id=user_id,
        user_tz=user_tz,
        active_today=active_today,
        blocked_without_output=blocked_without_output,
        endpoint_path=endpoint_path,
        request_id=request_id,
        has_output_today_override=has_out,
        today_override=today_iso,
    )
