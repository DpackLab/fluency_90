# app/schemas/registro_sesion.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegistroSesionCreate(BaseModel):
    inicio: datetime
    fin: Optional[datetime] = None

class RegistroSesionResponse(BaseModel):
    id: int
    usuario_id: int
    inicio: datetime
    fin: Optional[datetime]
    creado_en: datetime

    class Config:
        orm_mode = True
