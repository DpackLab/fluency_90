from sqlalchemy.orm import Session as DBSession
from datetime import datetime

from fluency90.models.session import Session as UserSession


def get_or_create_active_session(
    db: DBSession,
    user_id: int
) -> UserSession:
    """
    Returns an active session for the user.
    If none exists, creates one.
    """

    session = (
        db.query(UserSession)
        .filter(
            UserSession.user_id == user_id,
            UserSession.ended_at.is_(None)
        )
        .order_by(UserSession.started_at.desc())
        .first()
    )

    if session:
        return session

    session = UserSession(
        user_id=user_id,
        started_at=datetime.utcnow()
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session
