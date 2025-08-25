# tests/test_auth.py
from passlib.context import CryptContext

from app.models.idioma import Idioma
from app.models.usuario import Usuario

# Reusar el hasher en el módulo de test
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_admin(session):
    # Idioma base (upsert)
    lang = session.query(Idioma).filter_by(codigo_iso="en").one_or_none()
    if lang is None:
        lang = Idioma(nombre="Inglés", codigo_iso="en", descripcion="English")
        session.add(lang)
        session.commit()
        session.refresh(lang)

    # Usuario admin (idempotente)
    admin = session.query(Usuario).filter_by(email="admin@example.com").one_or_none()
    if admin is None:
        admin = Usuario(
            nombre="Admin",
            email="admin@example.com",
            contrasena=pwd_context.hash("Admin123!"),
            estilo="equilibrado",
            nivel_inicial="A2",
            idioma_id=lang.id,
        )
        session.add(admin)
    else:
        # Asegurar que la contraseña sea la del test
        admin.contrasena = pwd_context.hash("Admin123!")
        admin.idioma_id = lang.id

    session.commit()


def test_login_token(client, session):
    seed_admin(session)
    r = client.post(
        "/auth/token",
        data={"username": "admin@example.com", "password": "Admin123!"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert "access_token" in body and body["access_token"]
    assert body.get("token_type") == "bearer"
