# app/schemas/contenido_diario.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class ContenidoDiarioCreate(BaseModel):
    fecha: date = Field(..., example="2025-08-10")
    idioma_id: int
    contenido_id: Optional[int] = Field(
        None, description="ID opcional de un contenido ya existente"
    )
    objetivo_minutos: Optional[int] = Field(None, ge=1, le=180)
    notas: Optional[str] = None


class ContenidoDiarioResponse(BaseModel):
    id: int
    fecha: date
    idioma_id: int
    contenido_id: Optional[int]
    objetivo_minutos: Optional[int]
    notas: Optional[str]
    creado_en: datetime

    class Config:
        orm_mode = True
