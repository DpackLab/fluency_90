from sqlalchemy import Column, Integer, String
from app.database import Base


class Idioma(Base):
    __tablename__ = "idiomas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    codigo_iso = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)  # <-- NUEVA COLUMNA
