from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fluency90.core.config import settings


# Motor síncrono para PostgreSQL (psycopg)
engine = create_engine(
    settings.DATABASE_URL_SYNC,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para inyectar sesión de BD en los endpoints (modo síncrono).
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
