from pydantic import BaseModel
from typing import Optional

class IdiomaBase(BaseModel):
    nombre: str
    codigo_iso: str
    descripcion: Optional[str] = None  # ✅ nuevo campo opcional

class IdiomaCreate(IdiomaBase):
    pass

class IdiomaResponse(IdiomaBase):
    id: int

    class Config:
        orm_mode = True
