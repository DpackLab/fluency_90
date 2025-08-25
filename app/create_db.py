from app.database import Base, engine

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
