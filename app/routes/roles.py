# app/routes/roles.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.permissions import require_admin

from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.schemas.rol_schema import (
    RolCreate, RolResponse,
    UsuarioRolCreate, UsuarioRolResponse,
)

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RolResponse)
def crear_rol(
    payload: RolCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    rol = Rol(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

@router.get("/", response_model=list[RolResponse])
def listar_roles(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return db.query(Rol).all()

@router.post("/asignar", response_model=UsuarioRolResponse)
def asignar_rol(
    payload: UsuarioRolCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    ur = UsuarioRol(usuario_id=payload.usuario_id, rol_id=payload.rol_id)
    db.add(ur)
    db.commit()
    db.refresh(ur)
    return ur
