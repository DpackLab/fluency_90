from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.contenido import Contenido
from app.schemas.contenido import ContenidoCreate, ContenidoResponse
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.auth.token import verificar_token
from app.schemas.usuario_schema import UsuarioTokenData

router = APIRouter(prefix="/contenidos", tags=["Contenidos"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UsuarioTokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verificar_token(token, credentials_exception)

@router.post("/", response_model=ContenidoResponse)
def crear_contenido(
    contenido: ContenidoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user)
):
    nuevo_contenido = Contenido(
        titulo=contenido.titulo,
        tipo=contenido.tipo,
        url=contenido.url,
        descripcion=contenido.descripcion,
        idioma_id=contenido.idioma_id
    )
    db.add(nuevo_contenido)
    db.commit()
    db.refresh(nuevo_contenido)
    return nuevo_contenido

@router.get("/", response_model=list[ContenidoResponse])
def listar_contenidos(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user)
):
    return db.query(Contenido).all()
