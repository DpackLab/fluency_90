from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.idioma import Idioma
from app.schemas.idioma import IdiomaCreate, IdiomaResponse
from app.schemas.usuario_schema import UsuarioTokenData  # ✅ import corregido
from fastapi.security import OAuth2PasswordBearer
from app.auth.token import verificar_token

router = APIRouter(prefix="/idiomas", tags=["Idiomas"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UsuarioTokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verificar_token(token, credentials_exception)

@router.post("/", response_model=IdiomaResponse)
def crear_idioma(
    idioma: IdiomaCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user)
):
    db_idioma = db.query(Idioma).filter(Idioma.nombre == idioma.nombre).first()
    if db_idioma:
        raise HTTPException(status_code=400, detail="El idioma ya existe")

    nuevo_idioma = Idioma(
        nombre=idioma.nombre,
        codigo_iso=idioma.codigo_iso,
        descripcion=idioma.descripcion
    )
    db.add(nuevo_idioma)
    db.commit()
    db.refresh(nuevo_idioma)
    return nuevo_idioma

@router.get("/", response_model=list[IdiomaResponse])
def listar_idiomas(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user)
):
    return db.query(Idioma).all()
