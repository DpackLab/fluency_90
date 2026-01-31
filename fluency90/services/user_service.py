from sqlalchemy.orm import Session

from fluency90.models.user import User
from fluency90.schemas.user_schema import UserCreate
from fluency90.core.security import get_password_hash


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Crea un usuario nuevo.

    Reglas canónicas:
    - password SIEMPRE se hashea aquí
    - is_active se define internamente (no desde input)
    - role NO se acepta desde input (queda default 'user')
    """

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,  # control interno
        # role queda por default en DB / modelo
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
