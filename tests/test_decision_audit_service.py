from datetime import datetime, timezone

from fluency90.services.decision_audit_service import (
    list_recent_progress_decisions,
    get_last_progress_decision,
)


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return self._rows


class DummyDB:
    """
    DB stub mínimo: solo soporta db.execute(...).fetchall()
    """
    def __init__(self, rows):
        self._rows = rows

    def execute(self, *args, **kwargs):
        return _Result(self._rows)


def test_list_recent_progress_decisions_returns_shape():
    now = datetime(2026, 2, 23, 12, 0, 0, tzinfo=timezone.utc)

    rows = [
        (
            now,
            "progress_decision_evaluated",
            {
                "path": "/api/v1/users/me/stats",
                "allowed": False,
                "reason": "Output requerido para continuar",
                "signals": ["daily_state.blocked_without_output"],
                "request_id": "req-001",
                "today": "2026-02-23",
            },
        ),
    ]

    db = DummyDB(rows)

    out = list_recent_progress_decisions(db=db, user_id=16, limit=20)

    assert isinstance(out, list)
    assert len(out) == 1

    item = out[0]
    assert item["event_type"] == "progress_decision_evaluated"
    assert item["path"] == "/api/v1/users/me/stats"
    assert item["allowed"] is False
    assert item["reason"] == "Output requerido para continuar"
    assert item["signals"] == ["daily_state.blocked_without_output"]
    assert item["request_id"] == "req-001"
    assert "meta" in item


def test_get_last_progress_decision_none_when_empty():
    db = DummyDB([])
    last = get_last_progress_decision(db=db, user_id=16)
    assert last is None
