# app/routes/registro_sesiones.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioTokenData
from app.auth.token import get_current_user

from app.models.registro_sesion import RegistroSesion
from app.schemas.registro_sesion import (
    RegistroSesionCreate,
    RegistroSesionResponse,
)

router = APIRouter(prefix="/registro-sesiones", tags=["Métricas: sesiones"])


@router.post("/", response_model=RegistroSesionResponse)
def crear_registro_sesion(
    payload: RegistroSesionCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    registro = RegistroSesion(
        usuario_id=current_user.id,
        inicio=payload.inicio,
        fin=payload.fin,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


@router.get("/", response_model=list[RegistroSesionResponse])
def listar_registros(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    return (
        db.query(RegistroSesion)
        .filter(RegistroSesion.usuario_id == current_user.id)
        .all()
    )
