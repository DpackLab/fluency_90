# tests/test_contenidos.py
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


def _ensure_user(session, email="admin@example.com", password="Admin123!") -> Usuario:
    lang = _ensure_idioma(session)
    user = session.query(Usuario).filter_by(email=email).first()
    if not user:
        user = Usuario(
            nombre="Admin",
            email=email,
            contrasena=PWDCTX.hash(password),
            estilo="equilibrado",
            nivel_inicial="A2",
            idioma_id=lang.id,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def _login_token(client, email, password) -> str:
    r = client.post("/auth/token", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_contenidos_create_and_list(client, session):
    user = _ensure_user(session)  # usa admin@example.com
    token = _login_token(client, user.email, "Admin123!")
    lang = _ensure_idioma(session)

    # Crear
    payload = {
        "titulo": "mini podcast 01",
        "tipo": "audio",
        "url": "https://example.com/podcast01.mp3",
        "descripcion": "intro shadowing",
        "idioma_id": lang.id,
    }
    r = client.post(
        "/contenidos/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    created = r.json()
    assert created["titulo"] == payload["titulo"]
    assert created["idioma_id"] == lang.id

    # Listar
    r2 = client.get("/contenidos/", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200, r2.text
    items = r2.json()
    assert any(it["titulo"] == "mini podcast 01" for it in items)
