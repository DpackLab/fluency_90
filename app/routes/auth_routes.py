# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario import Usuario
from app.auth.token import crear_token
from app.core.ratelimit import limiter  # <- ¡importar desde core/ratelimit!

router = APIRouter(prefix="/auth", tags=["Autenticación"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def authenticate(db: Session, email: str, password: str) -> Usuario | None:
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.contrasena):
        return None
    return user


@router.post("/token")
@limiter.limit("10/minute")  # p.ej. 10 intentos/min por IP
def login_token(
    request: Request,  # <-- OBLIGATORIO cuando usas @limiter.limit
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# Si tienes otros endpoints con @limiter.limit, TODOS deben incluir request: Request
# Ejemplo:
@router.post("/register")
@limiter.limit("5/minute")
def register(
    request: Request,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    # ... implementación opcional de registro ...
    raise HTTPException(status_code=501, detail="No implementado aún")
