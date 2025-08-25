from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Contenido(Base):
    __tablename__ = "contenidos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Ej: "video", "audio", "texto"
    url = Column(String, nullable=False)
    descripcion = Column(String)
    idioma_id = Column(Integer, ForeignKey("idiomas.id"), nullable=False)
