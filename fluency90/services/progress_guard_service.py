from __future__ import annotations

from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from fluency90.services.daily_state_service import get_user_daily_state
from fluency90.services.progress_policy_service import decision_from_state
from fluency90.services.event_log_service import log_event


def enforce_progress_guard(
    *,
    db: Session,
    user_id: int,
    user_tz: Optional[str],
    endpoint_path: str,
    request_id: Optional[str] = None,
):
    """
    Guard canónico de progreso.

    Regla:
    - Los endpoints NO deciden.
    - Este guard obtiene el estado, consulta el motor y actúa.

    Comportamiento:
    - Si bloquea: log_event + HTTP 409
    - Si permite: retorna (state, decision) para uso mínimo del endpoint
    """

    state = get_user_daily_state(
        db=db,
        user_id=user_id,
        user_tz=user_tz or "UTC",
    )

    decision = decision_from_state(
        db=db,
        user_id=user_id,
        user_tz=user_tz,
        state=state,
        endpoint_path=endpoint_path,
        request_id=request_id,
    )

    # Observabilidad canónica: siempre registramos la evaluación (best-effort).
    # No cambia lógica ni contrato: solo deja evidencia de qué decidió el motor en el contexto del guard.
    try:
        log_event(
            db=db,
            event_type="progress_decision_evaluated",
            user_id=user_id,
            meta={
                "source": "guard",
                "path": endpoint_path,
                "request_id": request_id,
                "allowed": bool(getattr(decision, "allowed", False)),
                "reason": getattr(decision, "reason", None),
                "today": getattr(decision, "today", None),
                "signals": getattr(decision, "signals_used", None),
                # contexto mínimo del state (diagnóstico, no contrato público)
                "active_today": bool(getattr(state, "active_today", False)),
                "has_output_today": bool(getattr(state, "has_output_today", False)),
                "blocked_without_output": bool(getattr(state, "blocked_without_output", False)),
                "derived_state": getattr(state, "derived_state", None),
            },
        )
    except Exception:
        pass

    if not decision.allowed:
        # Observabilidad gobernada (best-effort)
        try:
            log_event(
                db=db,
                event_type="users_blocked_without_output",
                user_id=user_id,
                meta={
                    "source": "guard",
                    "path": endpoint_path,
                    "signals": decision.signals_used,
                    "today": decision.today,
                },
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=decision.reason or "Output requerido para continuar",
        )

    return state, decision
