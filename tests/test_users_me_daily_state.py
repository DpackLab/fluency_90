from datetime import date
from fastapi.testclient import TestClient

from main import app
import fluency90.core.security as security
import fluency90.api.v1.users as users_routes
import fluency90.services.progress_guard_service as guard_service


# Guardamos referencias originales para restaurar al final de cada test
_ORIG_GET_DAILY_STATE = users_routes.get_user_daily_state
_ORIG_DECISION_FROM_STATE = guard_service.decision_from_state
_ORIG_GUARD_LOG_EVENT = guard_service.log_event


def _override_current_user():
    class U:
        id = 16
        timezone = "America/Bogota"
        is_admin = False
    return U()


def _reset_overrides():
    users_routes.get_user_daily_state = _ORIG_GET_DAILY_STATE
    guard_service.decision_from_state = _ORIG_DECISION_FROM_STATE
    guard_service.log_event = _ORIG_GUARD_LOG_EVENT
    app.dependency_overrides = {}


def test_me_daily_state_does_not_block_even_if_decision_denies():
    """
    FRONTERA:
    /me/daily-state usa evaluate (NO enforce), por tanto NUNCA debe bloquear.
    Aunque la decisión del motor sea allowed=False, la respuesta debe ser 200.
    """
    client = TestClient(app)
    app.dependency_overrides[security.get_current_user] = _override_current_user

    def fake_get_user_daily_state(db, user_id: int, user_tz: str):
        class S:
            date = date(2026, 2, 16)
            active_today = True
            has_output_today = False
            blocked_without_output = True
            current_streak = 0
            session_active = True
            session_started_at = None
            derived_state = "ACTIVE_BLOCKED_NO_OUTPUT"
        return S()

    users_routes.get_user_daily_state = fake_get_user_daily_state

    def fake_decision_from_state(*args, **kwargs):
        class D:
            allowed = False
            reason = "Output requerido para continuar"
            today = "2026-02-16"
            signals_used = ["daily_state.blocked_without_output"]
        return D()

    guard_service.decision_from_state = fake_decision_from_state

    r = client.get("/api/v1/users/me/daily-state")
    assert r.status_code == 200

    body = r.json()
    assert body["active_today"] is True
    assert body["has_output_today"] is False
    assert body["blocked_without_output"] is True

    _reset_overrides()


def test_me_daily_state_survives_guard_log_event_failure_best_effort():
    """
    FRONTERA:
    Si el logging del guard falla (best-effort), el endpoint NO debe romper.
    Validamos que /me/daily-state sigue respondiendo 200.
    """
    client = TestClient(app)
    app.dependency_overrides[security.get_current_user] = _override_current_user

    def fake_get_user_daily_state(db, user_id: int, user_tz: str):
        class S:
            date = date(2026, 2, 16)
            active_today = True
            has_output_today = True
            blocked_without_output = False
            current_streak = 2
            session_active = True
            session_started_at = None
            derived_state = "ACTIVE_WITH_OUTPUT"
        return S()

    users_routes.get_user_daily_state = fake_get_user_daily_state

    def fake_decision_from_state(*args, **kwargs):
        class D:
            allowed = True
            reason = None
            today = "2026-02-16"
            signals_used = ["allow"]
        return D()

    guard_service.decision_from_state = fake_decision_from_state

    def boom_log_event(*args, **kwargs):
        raise RuntimeError("simulated log_event failure")

    # Esto afecta SOLO al log_event interno del guard (evaluate),
    # el endpoint aún debe responder 200.
    guard_service.log_event = boom_log_event

    r = client.get("/api/v1/users/me/daily-state")
    assert r.status_code == 200

    body = r.json()
    assert body["active_today"] is True
    assert body["has_output_today"] is True
    assert body["blocked_without_output"] is False

    _reset_overrides()
