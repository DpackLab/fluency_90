# app/models/usuario_rol.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
