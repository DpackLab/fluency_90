# app/models/registro_sesion.py
# -----------------------------
# Registro de sesiones de uso (inicio/fin) por usuario.
# -----------------------------

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class RegistroSesion(Base):
    __tablename__ = "registro_sesiones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    inicio = Column(DateTime(timezone=True), nullable=False)  # timestamp inicio
    fin = Column(
        DateTime(timezone=True), nullable=True
    )  # timestamp fin (puede cerrarse más tarde)
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
