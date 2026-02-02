from fastapi.testclient import TestClient

from main import app
import fluency90.core.security as security
import fluency90.api.v1.users as users_routes
import fluency90.services.progress_guard_service as guard_service

# Guardamos referencias originales para restaurar al final de cada test
_ORIG_GET_STATS = users_routes.get_user_me_stats
_ORIG_DAILY_STATE = users_routes.get_user_daily_state

class Decision:
    def __init__(self, allowed: bool, reason: str = "", has_output_today: bool = False):
        self.allowed = allowed
        self.reason = reason
        self.has_output_today = has_output_today

def _override_current_user():
    class U:
        id = 16
        timezone = "America/Bogota"
        is_admin = False
    return U()

def _reset_overrides():
    users_routes.get_user_me_stats = _ORIG_GET_STATS
    users_routes.get_user_daily_state = _ORIG_DAILY_STATE
    app.dependency_overrides = {}

def _get_route_endpoint(path: str):
    for route in app.router.routes:
        if getattr(route, "path", None) == path:
            return route.endpoint
    raise RuntimeError(f"Route not found for path={path}")

def test_me_stats_active_no_output_returns_409():
    client = TestClient(app)
    app.dependency_overrides[security.get_current_user] = _override_current_user

    # 1) Daily state simulado: ESTO decide el 409 hoy
    def fake_get_user_daily_state(db, user_id: int, user_tz: str):
        class S:
            blocked_without_output = True
        return S()

    guard_service.get_user_daily_state = fake_get_user_daily_state

    # 2) Stats simulados: no deciden el 409, pero cumplen contrato si llegara a serializarse
    def fake_get_user_me_stats(db, user_id: int, user_tz: str):
        return {
            "current_streak": 0,
            "active_today": True,
            "session_active": False,
            "session_started_at": None,
            "has_output_today": False,
            "blocked_without_output": True,
        }

    users_routes.get_user_me_stats = fake_get_user_me_stats

    # 3) Llamada al endpoint
    r = client.get("/api/v1/users/me/stats")
    assert r.status_code == 409
    assert r.json()["detail"] == "Output requerido para continuar"

    _reset_overrides()

def test_me_stats_active_with_output_returns_200():
    client = TestClient(app)
    app.dependency_overrides[security.get_current_user] = _override_current_user

    def fake_get_user_me_stats(db, user_id: int, user_tz: str):
        # OJO: si tu endpoint “inyecta” estos campos, aquí podrías omitirlos.
        # En tu implementación actual, el endpoint retorna stats tal cual.
        return {
            "current_streak": 2,
            "active_today": True,
            "session_active": False,
            "session_started_at": None,
            "has_output_today": True,
            "blocked_without_output": False,
        }

    users_routes.get_user_me_stats = fake_get_user_me_stats

    def fake_get_user_daily_state(db, user_id: int, user_tz: str):
        class S:
            active_today = True
            has_output_today = True
            blocked_without_output = False
            date = None
            current_streak = 2
            session_active = False
            session_started_at = None
            derived_state = "ACTIVE_WITH_OUTPUT"
        return S()

    guard_service.get_user_daily_state = fake_get_user_daily_state

    def fake_decision_from_state(*args, **kwargs):
        class D:
            allowed = True
            reason = None
            has_output_today = True
            today = "2026-01-31"
            signals_used = ["allow"]
        return D()

    guard_service.decision_from_state = fake_decision_from_state

    r = client.get("/api/v1/users/me/stats")
    assert r.status_code == 200

    body = r.json()
    assert body["active_today"] is True
    assert body["has_output_today"] is True
    assert body["blocked_without_output"] is False

    _reset_overrides()


def test_me_stats_inactive_no_output_returns_200():
    client = TestClient(app)
    app.dependency_overrides[security.get_current_user] = _override_current_user

    def fake_get_user_me_stats(db, user_id: int, user_tz: str):
        return {
            "current_streak": 0,
            "active_today": False,
            "session_active": False,
            "session_started_at": None,
            "has_output_today": False,
            "blocked_without_output": False,
        }

    users_routes.get_user_me_stats = fake_get_user_me_stats

    def fake_evaluate_progress_state(*args, **kwargs):
        return Decision(
            allowed=True,
            reason="",
            has_output_today=False,
        )

    def fake_get_user_daily_state(db, user_id: int, user_tz: str):
        class S:
            active_today = False
            has_output_today = False
            blocked_without_output = False
            date = None
            current_streak = 0
            session_active = False
            session_started_at = None
            derived_state = "INACTIVE_NO_OUTPUT"
        return S()

    guard_service.get_user_daily_state = fake_get_user_daily_state

    def fake_decision_from_state(*args, **kwargs):
        class D:
            allowed = True
            reason = None
            has_output_today = False
            today = "2026-01-31"
            signals_used = ["allow"]
        return D()

    guard_service.decision_from_state = fake_decision_from_state

    r = client.get("/api/v1/users/me/stats")
    assert r.status_code == 200

    body = r.json()
    assert body["active_today"] is False
    assert body["has_output_today"] is False
    assert body["blocked_without_output"] is False

    _reset_overrides()
