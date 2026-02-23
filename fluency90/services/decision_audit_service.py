from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session


def list_recent_progress_decisions(
    *,
    db: Session,
    user_id: int,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """
    Read-only: trae decisiones recientes del guard desde event_log.

    Fuente de verdad:
    - event_log (event_type = 'progress_decision_evaluated')
    - occurred_at (orden descendente)

    NO toca motor, NO toca guard, NO cambia contratos.
    """
    lim = int(limit) if limit and int(limit) > 0 else 20

    rows = db.execute(
        text(
            """
            SELECT occurred_at, event_type, meta
            FROM event_log
            WHERE user_id = :user_id
              AND event_type = 'progress_decision_evaluated'
            ORDER BY occurred_at DESC
            LIMIT :limit
            """
        ),
        {"user_id": user_id, "limit": lim},
    ).fetchall()

    out: List[Dict[str, Any]] = []
    for r in rows:
        occurred_at = r[0]
        event_type = r[1]
        meta = r[2] or {}

        # meta puede venir como dict (jsonb) o como string dependiendo del driver/config.
        if isinstance(meta, str):
            # Best-effort: no rompemos lectura si meta viene como string.
            try:
                import json  # local import para no contaminar el módulo
                meta = json.loads(meta)
            except Exception:
                meta = {"raw_meta": meta}

        out.append(
            {
                "occurred_at": occurred_at,
                "event_type": event_type,
                "path": meta.get("path"),
                "allowed": meta.get("allowed"),
                "reason": meta.get("reason"),
                "signals": meta.get("signals"),
                "request_id": meta.get("request_id"),
                "today": meta.get("today"),
                "meta": meta,
            }
        )

    return out


def get_last_progress_decision(
    *,
    db: Session,
    user_id: int,
) -> Optional[Dict[str, Any]]:
    """
    Read-only helper: última decisión o None.
    """
    rows = list_recent_progress_decisions(db=db, user_id=user_id, limit=1)
    return rows[0] if rows else None
