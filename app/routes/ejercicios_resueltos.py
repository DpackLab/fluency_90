# app/routes/ejercicios_resueltos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioTokenData
from app.auth.token import get_current_user

from app.models.ejercicio_resuelto import EjercicioResuelto
from app.schemas.ejercicio_resuelto import (
    EjercicioResueltoCreate,
    EjercicioResueltoResponse,
)

router = APIRouter(prefix="/ejercicios-resueltos", tags=["Métricas: ejercicios"])

@router.post("/", response_model=EjercicioResueltoResponse)
def crear_ejercicio_resuelto(
    payload: EjercicioResueltoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    registro = EjercicioResuelto(
        usuario_id=current_user.id,
        reto_id=payload.reto_id,
        tipo=payload.tipo,
        wpm=payload.wpm,
        comprension_pct=payload.comprension_pct,
        errores_por_min=payload.errores_por_min,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro

@router.get("/", response_model=list[EjercicioResueltoResponse])
def listar_ejercicios_resueltos(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    return (
        db.query(EjercicioResuelto)
        .filter(EjercicioResuelto.usuario_id == current_user.id)
        .all()
    )
