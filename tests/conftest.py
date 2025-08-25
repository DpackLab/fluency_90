# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# 👇 IMPORTA TODOS LOS MODELOS para que queden registrados en Base.metadata
# (tu app/models/__init__.py ya reexporta las clases, esto fuerza su import)
from app import models  # noqa: F401

# Un SQLite de archivo (mismo proceso/hilo lo ve todo)
SQLALCHEMY_DATABASE_URL = "sqlite:///./_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_db():
    # arrancamos limpio y con TODAS las tablas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Forzamos a la app a usar *exactamente* esta sesión de tests
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
