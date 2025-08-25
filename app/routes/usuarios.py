from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioTokenData
from app.auth.token import get_current_user  # JWT

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(
        get_current_user
    ),  # si quieres que crear requiera login
):
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contrasena=get_password_hash(usuario.contrasena),  # hashear SIEMPRE
        estilo=usuario.estilo,
        nivel_inicial=usuario.nivel_inicial,
        idioma_id=usuario.idioma_id,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo  # responde sin contraseña gracias a UsuarioResponse


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    return db.query(Usuario).all()
