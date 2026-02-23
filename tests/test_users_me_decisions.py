from fastapi.testclient import TestClient

from main import app
import fluency90.core.security as security
import fluency90.api.v1.users as users_routes
import fluency90.services.progress_guard_service as guard_service

# Guardamos originales
_ORIG_LIST_DECISIONS = users_routes.list_recent_progress_decisions
_ORIG_DAILY_STATE = guard_service.get_user_daily_state
_ORIG_DECISION_FROM_STATE = guard_service.decision_from_state


def _override_current_user():
    class U:
        id = 16
        timezone = "America/Bogota"
        is_admin = False
    return U()


def _reset():
    users_routes.list_recent_progress_decisions = _ORIG_LIST_DECISIONS
    guard_service.get_user_daily_state = _ORIG_DAILY_STATE
    guard_service.decision_from_state = _ORIG_DECISION_FROM_STATE
    app.dependency_overrides = {}


def test_me_decisions_returns_200_even_if_motor_denies():
    """
    /me/decisions usa evaluate, por tanto NO debe bloquear aunque allowed=False.
    """
    client = TestClient(app)
    app.dependency_overrides[security.get_current_user] = _override_current_user

    # Forzamos un state "bloqueante"
    def fake_get_user_daily_state(db, user_id: int, user_tz: str):
        class S:
            active_today = True
            has_output_today = False
            blocked_without_output = True
            derived_state = "ACTIVE_BLOCKED_NO_OUTPUT"
        return S()

    guard_service.get_user_daily_state = fake_get_user_daily_state

    # Forzamos motor deny
    def fake_decision_from_state(*args, **kwargs):
        class D:
            allowed = False
            reason = "Output requerido para continuar"
            today = "2026-02-23"
            signals_used = ["daily_state.blocked_without_output"]
        return D()

    guard_service.decision_from_state = fake_decision_from_state

    # Respuesta del audit service (stub)
    def fake_list_recent_progress_decisions(*, db, user_id: int, limit: int = 20):
        return [
            {
                "event_type": "progress_decision_evaluated",
                "path": "/api/v1/users/me/stats",
                "allowed": False,
                "reason": "Output requerido para continuar",
                "signals": ["daily_state.blocked_without_output"],
                "request_id": "req-001",
                "today": "2026-02-23",
            }
        ]

    users_routes.list_recent_progress_decisions = fake_list_recent_progress_decisions

    r = client.get("/api/v1/users/me/decisions?limit=10")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert body[0]["event_type"] == "progress_decision_evaluated"

    _reset()
