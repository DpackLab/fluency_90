# app/models/reto.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Reto(Base):
    __tablename__ = "retos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    dificultad = Column(String(50), nullable=True)
    # Mantener idioma_id sin forzar por ahora (pendiente decisión de negocio)
    # Si ya existe la columna, no tocar; si no existe y la quieres, la añadimos luego con migración.
    # idioma_id = Column(Integer, ForeignKey("idiomas.id"), nullable=True)
    activo = Column(Boolean, nullable=False, server_default="true")
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
