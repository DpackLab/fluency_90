from app.database import Base, engine
from app.models import usuario, idioma

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
