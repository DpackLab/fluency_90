from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Para la protección JWT


# Esquema base para entrada de datos (POST)
class RetoCreate(BaseModel):
    titulo: str = Field(..., example="Reto de vocabulario básico")
    descripcion: Optional[str] = Field(None, example="Practica palabras básicas")
    dificultad: Optional[str] = Field(None, example="Fácil")
    activo: Optional[bool] = Field(default=True)


# Esquema de respuesta para salida de datos (GET)
class RetoResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    dificultad: Optional[str]
    activo: bool
    creado_en: datetime

    class Config:
        orm_mode = True
