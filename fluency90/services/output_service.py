from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy.orm import Session as DBSession
from fastapi import HTTPException, status

from fluency90.models.user_output import UserOutput
from fluency90.services.active_day_service import mark_user_active_today

MIN_OUTPUT_TEXT_LEN = 20

def _validate_output_payload(output_type: str, payload: dict) -> dict:
    if not output_type or not isinstance(output_type, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="output_type inválido",
        )

    ot = output_type.strip().lower()

    if ot == "text":
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="payload inválido para output_type=text",
            )

        text = payload.get("text")
        if not isinstance(text, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="payload.text es requerido y debe ser string",
            )

        clean = text.strip()
        if len(clean) < MIN_OUTPUT_TEXT_LEN:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Output no cumple criterios mínimos (min {MIN_OUTPUT_TEXT_LEN} caracteres)",
            )

        payload["text"] = clean
        return payload

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"output_type '{ot}' no soportado",
    )

def create_user_output(
    db: DBSession,
    user_id: int,
    user_tz: str,
    output_type: str,
    payload: dict,
) -> UserOutput:

    # ✅ Validación semántica (no muta payload)
    _validate_output_payload(output_type=output_type, payload=payload)

    # 1) Persistir output
    rec = UserOutput(
        user_id=user_id,
        output_type=output_type,
        payload=payload,
        created_at=datetime.now(timezone.utc),
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    # 2) Impacto en métricas SIN duplicar estado
    mark_user_active_today(db, user_id, user_tz)

    return rec

