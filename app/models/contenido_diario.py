# app/models/contenido_diario.py
# --------------------------------
# Programación diaria de contenido por idioma y/o contenido base.
# Permite definir un objetivo de minutos y enlazar a un contenido existente.
# --------------------------------

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class ContenidoDiario(Base):
    __tablename__ = "contenidos_diarios"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)                         # Día programado (YYYY-MM-DD)
    idioma_id = Column(Integer, ForeignKey("idiomas.id"), nullable=False)
    contenido_id = Column(Integer, ForeignKey("contenidos.id"), nullable=True)  # Opcional: liga a un contenido
    objetivo_minutos = Column(Integer, nullable=True)            # Meta sugerida de práctica
    notas = Column(String, nullable=True)                        # Notas libres / pauta del día
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
