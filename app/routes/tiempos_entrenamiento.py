# app/routes/tiempos_entrenamiento.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioTokenData
from app.auth.token import get_current_user

from app.models.tiempo_entrenamiento import TiempoEntrenamiento
from app.schemas.tiempo_entrenamiento import (
    TiempoEntrenamientoCreate,
    TiempoEntrenamientoResponse,
)

router = APIRouter(prefix="/tiempos-entrenamiento", tags=["Métricas: tiempo"])


@router.post("/", response_model=TiempoEntrenamientoResponse)
def crear_tiempo(
    payload: TiempoEntrenamientoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    registro = TiempoEntrenamiento(
        usuario_id=current_user.id,
        fecha=payload.fecha,
        minutos=payload.minutos,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


@router.get("/", response_model=list[TiempoEntrenamientoResponse])
def listar_tiempos(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    return (
        db.query(TiempoEntrenamiento)
        .filter(TiempoEntrenamiento.usuario_id == current_user.id)
        .all()
    )
