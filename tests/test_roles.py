# tests/test_roles.py
from passlib.context import CryptContext
from app.models.idioma import Idioma
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol

PWDCTX = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _ensure_idioma(session) -> Idioma:
    lang = session.query(Idioma).filter_by(codigo_iso="en").first()
    if not lang:
        lang = Idioma(nombre="Inglés", codigo_iso="en", descripcion="English")
        session.add(lang)
        session.commit()
        session.refresh(lang)
    return lang


def _ensure_user(session, email, password) -> Usuario:
    lang = _ensure_idioma(session)
    user = session.query(Usuario).filter_by(email=email).first()
    if not user:
        user = Usuario(
            nombre=email.split("@")[0],
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


def _ensure_admin_role(session) -> Rol:
    role = session.query(Rol).filter_by(nombre="admin").first()
    if not role:
        role = Rol(nombre="admin", descripcion="Superusuario")
        session.add(role)
        session.commit()
        session.refresh(role)
    return role


def _grant_admin(session, user: Usuario):
    role = _ensure_admin_role(session)
    if not session.query(UsuarioRol).filter_by(usuario_id=user.id, rol_id=role.id).first():
        session.add(UsuarioRol(usuario_id=user.id, rol_id=role.id))
        session.commit()
    return role


def _login_token(client, email, password) -> str:
    r = client.post("/auth/token", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_roles_assign_with_admin(client, session):
    # Admin + token
    admin = _ensure_user(session, "admin@example.com", "Admin123!")
    _grant_admin(session, admin)
    token_admin = _login_token(client, admin.email, "Admin123!")

    # Usuario a promover
    user = _ensure_user(session, "user2@example.com", "User123!")
    role = _ensure_admin_role(session)

    # Asignar rol
    payload = {"usuario_id": user.id, "rol_id": role.id}
    r = client.post(
        "/roles/asignar",
        json=payload,
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["usuario_id"] == user.id
    assert body["rol_id"] == role.id
