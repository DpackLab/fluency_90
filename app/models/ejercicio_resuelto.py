# app/models/ejercicio_resuelto.py
# --------------------------------
# Métrica de ejercicios/retos realizados con calidad.
# --------------------------------

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class EjercicioResuelto(Base):
    __tablename__ = "ejercicios_resueltos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    reto_id = Column(Integer, ForeignKey("retos.id"), nullable=True)      # opcional si se asocia a un reto
    tipo = Column(String, nullable=True)                                   # p.ej. "shadowing", "listening"
    wpm = Column(Float, nullable=True)                                     # palabras por minuto
    comprension_pct = Column(Float, nullable=True)                         # 0-100
    errores_por_min = Column(Float, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
