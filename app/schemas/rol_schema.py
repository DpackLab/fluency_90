# app/schemas/rol_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RolCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True


class UsuarioRolCreate(BaseModel):
    usuario_id: int
    rol_id: int


class UsuarioRolResponse(BaseModel):
    id: int
    usuario_id: int
    rol_id: int
    creado_en: datetime

    class Config:
        orm_mode = True
