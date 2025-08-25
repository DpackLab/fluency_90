# app/models/tiempo_entrenamiento.py
# ----------------------------------
# Agregado diario de minutos de entrenamiento por usuario.
# ----------------------------------

from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class TiempoEntrenamiento(Base):
    __tablename__ = "tiempos_entrenamiento"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    minutos = Column(Integer, nullable=False)  # total minutos del día
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
