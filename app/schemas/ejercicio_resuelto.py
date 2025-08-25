# app/schemas/ejercicio_resuelto.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EjercicioResueltoCreate(BaseModel):
    reto_id: Optional[int] = None
    tipo: Optional[str] = Field(None, example="shadowing")
    wpm: Optional[float] = None
    comprension_pct: Optional[float] = Field(None, ge=0, le=100)
    errores_por_min: Optional[float] = Field(None, ge=0)


class EjercicioResueltoResponse(BaseModel):
    id: int
    usuario_id: int
    reto_id: Optional[int]
    tipo: Optional[str]
    wpm: Optional[float]
    comprension_pct: Optional[float]
    errores_por_min: Optional[float]
    creado_en: datetime

    class Config:
        orm_mode = True
