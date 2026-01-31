from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fluency90.core.database import get_db
from fluency90.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from fluency90.models import User, Token as TokenModel
from fluency90.schemas.token_schema import Token
from fluency90.services.event_log_service import log_event

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Path canónico (sin slash final)
    path = "/api/v1/auth/login"

    # Buscar usuario por email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Observabilidad: intento fallido (best effort)
        log_event(
            db=db,
            event_type="auth_login_failed",
            user_id=None,
            meta={"source": "api", "path": path, "reason": "invalid_credentials"},
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Observabilidad: login exitoso (best effort)
    log_event(
        db=db,
        event_type="auth_login",
        user_id=user.id,
        meta={"source": "api", "path": path},
    )

    # Crear tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    # Guardar token en BD (opcional pero recomendado)
    token_db = TokenModel(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    db.add(token_db)
    db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
