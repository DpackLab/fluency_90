# tests/test_tiempos.py
from passlib.context import CryptContext
from app.models.idioma import Idioma
from app.models.usuario import Usuario

PWDCTX = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _ensure_idioma(session) -> Idioma:
    lang = session.query(Idioma).filter_by(codigo_iso="en").first()
    if not lang:
        lang = Idioma(nombre="Inglés", codigo_iso="en", descripcion="English")
        session.add(lang)
        session.commit()
        session.refresh(lang)
    return lang


def _ensure_user(session, email="user@example.com", password="User123!") -> Usuario:
    _ensure_idioma(session)
    user = session.query(Usuario).filter_by(email=email).first()
    if not user:
        user = Usuario(
            nombre="User",
            email=email,
            contrasena=PWDCTX.hash(password),
            estilo="equilibrado",
            nivel_inicial="A2",
            idioma_id=session.query(Idioma).filter_by(codigo_iso="en").first().id,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def _login_token(client, email, password) -> str:
    r = client.post("/auth/token", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_tiempos_requires_token(client):
    payload = {"fecha": "2025-08-12", "minutos": 30}
    r = client.post("/tiempos-entrenamiento/", json=payload)
    assert r.status_code == 401  # Not authenticated


def test_tiempos_with_token(client, session):
    user = _ensure_user(session)
    token = _login_token(client, user.email, "User123!")
    payload = {"fecha": "2025-08-12", "minutos": 30}

    r = client.post(
        "/tiempos-entrenamiento/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["minutos"] == 30
    assert body["usuario_id"] == user.id
