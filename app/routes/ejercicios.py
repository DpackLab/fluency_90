from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioSchema, UsuarioTokenData
from app.models.usuario_model import Usuario
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.auth.token import verificar_token

router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UsuarioTokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verificar_token(token, credentials_exception)


@router.post("/", summary="Crear Usuario")
def crear_usuario(
    usuario: UsuarioSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    db_usuario = Usuario(nombre=usuario.nombre, correo=usuario.correo)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
