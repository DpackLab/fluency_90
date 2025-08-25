# app/routes/contenidos_diarios.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioTokenData
from app.auth.token import get_current_user

from app.models.contenido_diario import ContenidoDiario
from app.schemas.contenido_diario import (
    ContenidoDiarioCreate,
    ContenidoDiarioResponse,
)

router = APIRouter(prefix="/contenidos-diarios", tags=["Contenidos diarios"])


@router.post("/", response_model=ContenidoDiarioResponse)
def crear_contenido_diario(
    payload: ContenidoDiarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    registro = ContenidoDiario(
        fecha=payload.fecha,
        idioma_id=payload.idioma_id,
        contenido_id=payload.contenido_id,
        objetivo_minutos=payload.objetivo_minutos,
        notas=payload.notas,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


@router.get("/", response_model=list[ContenidoDiarioResponse])
def listar_contenidos_diarios(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    return db.query(ContenidoDiario).all()
