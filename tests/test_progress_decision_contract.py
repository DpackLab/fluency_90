import pytest
from datetime import date

from fluency90.services.progress_policy_service import decision_from_state
from fluency90.services.daily_state_service import UserDailyState


class DummyDB:
    """
    DB mínima para validar contrato.
    El motor NO debe depender de DB cuando recibe state.
    """
    pass


def make_state(
    *,
    active_today: bool,
    has_output_today: bool,
    blocked_without_output: bool,
    derived_state: str = "TEST_STATE",
):
    return UserDailyState(
        date=date(2026, 1, 31),
        active_today=active_today,
        has_output_today=has_output_today,
        blocked_without_output=blocked_without_output,
        current_streak=0,
        session_active=False,
        session_started_at=None,
        derived_state=derived_state,
    )


def test_contract_blocked_when_active_without_output():
    """
    CONTRATO:
    Si el usuario está activo hoy y no tiene output,
    la decisión DEBE ser bloqueo.
    """
    state = make_state(
        active_today=True,
        has_output_today=False,
        blocked_without_output=True,
    )

    decision = decision_from_state(
        db=DummyDB(),
        user_id=1,
        user_tz="UTC",
        state=state,
        endpoint_path="/contract-test",
        request_id="req-001",
    )

    assert decision.allowed is False
    assert decision.reason == "Output requerido para continuar"


def test_contract_allowed_when_active_with_output():
    """
    CONTRATO:
    Usuario activo con output → permitido.
    """
    state = make_state(
        active_today=True,
        has_output_today=True,
        blocked_without_output=False,
    )

    decision = decision_from_state(
        db=DummyDB(),
        user_id=1,
        user_tz="UTC",
        state=state,
        endpoint_path="/contract-test",
        request_id="req-002",
    )

    assert decision.allowed is True
    assert decision.reason is None


def test_contract_allowed_when_inactive():
    """
    CONTRATO:
    Usuario no activo hoy → permitido.
    """
    state = make_state(
        active_today=False,
        has_output_today=False,
        blocked_without_output=False,
    )

    decision = decision_from_state(
        db=DummyDB(),
        user_id=1,
        user_tz="UTC",
        state=state,
        endpoint_path="/contract-test",
        request_id="req-003",
    )

    assert decision.allowed is True
    assert decision.reason is None
