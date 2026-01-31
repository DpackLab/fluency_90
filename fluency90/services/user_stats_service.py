from sqlalchemy.orm import Session as DBSession

from fluency90.services.daily_state_service import get_user_daily_state


def get_user_me_stats(db: DBSession, user_id: int, user_tz: str) -> dict:
    """
    Lector canónico de stats del usuario.
    Delegamos TODA la lógica diaria a daily_state_service.
    """

    state = get_user_daily_state(
        db=db,
        user_id=user_id,
        user_tz=user_tz,
    )

    return {
        "current_streak": state.current_streak,
        "active_today": state.active_today,
        "session_active": state.session_active,
        "session_started_at": state.session_started_at,
        "has_output_today": state.has_output_today,
        "blocked_without_output": state.blocked_without_output,
        # derived_state se mantiene backend-only (NO exponer)
    }
