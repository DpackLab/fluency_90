# app/models/rol.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)  # 'admin', 'usuario'
    descripcion = Column(String, nullable=True)
