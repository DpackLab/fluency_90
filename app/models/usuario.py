# app/models/usuario.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    estilo = Column(String, nullable=False)
    nivel_inicial = Column(String, nullable=False)
    idioma_id = Column(Integer, ForeignKey("idiomas.id"), nullable=False)
    # ✅ Consistente con el resto de tablas (timezone y server_default)
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
