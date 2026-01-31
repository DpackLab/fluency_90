from __future__ import annotations

import json
import sys
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import text


def _normalize_path(path: Optional[str]) -> Optional[str]:
    """
    Normaliza paths para observabilidad.
    Regla: quitar slash final (excepto si es "/").
    """
    if not path:
        return path
    if path == "/":
        return path
    return path.rstrip("/")


def log_event(
    db: Session,
    event_type: str,
    user_id: Optional[int] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Inserta un evento canónico en la tabla event_log.

    Reglas:
    - No falla el request si el logging falla (best effort).
    - No agrega dependencias ni modelos nuevos hoy.
    - Si falla, deja evidencia mínima en stderr (operable en Ubuntu/terminal).
    """
    try:
        meta_clean = None
        if meta is not None:
            meta_clean = dict(meta)  # copia defensiva
            if "path" in meta_clean:
                meta_clean["path"] = _normalize_path(str(meta_clean.get("path")))

        payload = None if meta_clean is None else json.dumps(meta_clean, ensure_ascii=False, default=str)

        # Validación previa: si event_type no existe o está inactivo, no intentamos insertar
        exists_row = db.execute(
            text(
                "SELECT 1 FROM event_types "
                "WHERE event_type = :event_type AND is_active = true "
                "LIMIT 1"
            ),
            {"event_type": event_type},
        ).first()

        if exists_row is None:
            sys.stderr.write(
                f"[event_log_service] log_event SKIPPED: event_type not in event_types or inactive: {event_type}\n"
            )
            return

        db.execute(
            text(
                "INSERT INTO event_log (event_type, user_id, meta) "
                "VALUES (:event_type, :user_id, CAST(:meta AS jsonb))"
            ),
            {"event_type": event_type, "user_id": user_id, "meta": payload},
        )
        db.commit()

    except Exception as e:
        # Best effort: no bloquear el flujo principal por observabilidad
        try:
            db.rollback()
        except Exception:
            pass

        try:
            sys.stderr.write(
                f"[event_log_service] log_event FAILED: event_type={event_type} user_id={user_id} err={e}\n"
            )
        except Exception:
            pass

