# bootstrap_admin.py
import os
import argparse
import secrets
import string

from passlib.context import CryptContext
from app.database import SessionLocal
from app.models.idioma import Idioma
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _create_or_get_admin(db, email: str, password: str, lang_code: str):
    # 1) Idioma base
    lang = db.query(Idioma).filter_by(codigo_iso=lang_code).first()
    if not lang:
        nombre = "Inglés" if lang_code == "en" else lang_code.upper()
        lang = Idioma(nombre=nombre, codigo_iso=lang_code, descripcion=None)
        db.add(lang)
        db.commit()
        db.refresh(lang)

    # 2) Usuario admin
    user = db.query(Usuario).filter_by(email=email).first()
    if not user:
        user = Usuario(
            nombre="Admin",
            email=email,
            contrasena=pwd_context.hash(password),
            estilo="equilibrio",
            nivel_inicial="A2",
            idioma_id=lang.id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 3) Rol admin
    role = db.query(Rol).filter_by(nombre="admin").first()
    if not role:
        role = Rol(nombre="admin", descripcion="Superusuario")
        db.add(role)
        db.commit()
        db.refresh(role)

    # 4) Asignación rol→usuario
    link = db.query(UsuarioRol).filter_by(usuario_id=user.id, rol_id=role.id).first()
    if not link:
        db.add(UsuarioRol(usuario_id=user.id, rol_id=role.id))
        db.commit()

    return user, role


def main(run_flag: bool, email: str, password: str | None, lang_code: str):
    # 🔒 Deshabilitado por defecto
    allowed = run_flag or os.getenv("BOOTSTRAP_ADMIN", "0") in (
        "1",
        "true",
        "True",
        "yes",
        "YES",
    )
    if not allowed:
        print(
            "🔒 Bootstrap deshabilitado. Para ejecutarlo usa:\n"
            "   python bootstrap_admin.py --run\n"
            "o exporta temporalmente BOOTSTRAP_ADMIN=1 y luego ejecuta el script.\n"
        )
        return

    generated = False
    if not password:
        alphabet = string.ascii_letters + string.digits + "!@#$%_-"
        password = "".join(secrets.choice(alphabet) for _ in range(16))
        generated = True

    db = SessionLocal()
    try:
        user, role = _create_or_get_admin(
            db, email=email, password=password, lang_code=lang_code
        )
        print("\n✅ Admin creado o verificado:")
        print(f"   email:    {user.email}")
        msg = "   password: " + password
        if generated:
            msg += "  (generada automáticamente, cámbiala cuanto antes)"
        print(msg + "\n")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crea/verifica un usuario admin. DESHABILITADO por defecto."
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Ejecutar realmente el bootstrap (override del bloqueo).",
    )
    parser.add_argument(
        "--email", default=os.getenv("BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    )
    parser.add_argument(
        "--password",
        default=os.getenv("BOOTSTRAP_ADMIN_PASSWORD"),
        help="Si no se especifica, se genera una aleatoria segura.",
    )
    parser.add_argument(
        "--lang", dest="lang_code", default=os.getenv("BOOTSTRAP_LANG", "en")
    )
    args = parser.parse_args()

    main(
        run_flag=args.run,
        email=args.email,
        password=args.password,
        lang_code=args.lang_code,
    )
