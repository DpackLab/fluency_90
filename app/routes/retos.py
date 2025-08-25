# app/routes/retos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.reto import Reto
from app.schemas.reto_schema import RetoCreate, RetoResponse
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.auth.token import verificar_token
from app.schemas.usuario_schema import UsuarioTokenData

router = APIRouter(prefix="/retos", tags=["Retos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UsuarioTokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verificar_token(token, credentials_exception)

@router.post("/", response_model=RetoResponse)
def crear_reto(
    reto: RetoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user)
):
    nuevo = Reto(
        titulo=reto.titulo,
        descripcion=reto.descripcion,
        dificultad=reto.dificultad,
        activo=(reto.activo if reto.activo is not None else True),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[RetoResponse])
def listar_retos(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user)
):
    return db.query(Reto).all()
