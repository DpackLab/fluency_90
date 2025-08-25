from pydantic import BaseModel
from typing import Optional


class ContenidoCreate(BaseModel):
    titulo: str
    tipo: str
    url: str
    descripcion: Optional[str] = None
    idioma_id: int


class ContenidoResponse(BaseModel):
    id: int
    titulo: str
    tipo: str
    url: str
    descripcion: Optional[str] = None
    idioma_id: int

    class Config:
        orm_mode = True
