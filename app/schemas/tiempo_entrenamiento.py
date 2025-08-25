# app/schemas/tiempo_entrenamiento.py
from pydantic import BaseModel, Field
from datetime import date, datetime

class TiempoEntrenamientoCreate(BaseModel):
    fecha: date
    minutos: int = Field(..., ge=1, le=600)

class TiempoEntrenamientoResponse(BaseModel):
    id: int
    usuario_id: int
    fecha: date
    minutos: int
    creado_en: datetime

    class Config:
        orm_mode = True
