import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Hacer que 'app' sea importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cargar variables de entorno desde .env (opcional)
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# Configuración Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Si existe DATABASE_URL en el entorno, úsala
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# --- Registrar metadatos y tablas -------------------------------
# Importar Base y TODOS los modelos para que Alembic vea las tablas.
from app.database import Base  # noqa: E402
import app.models  # noqa: F401, E402  # side-effect: registra todas las tablas

target_metadata = Base.metadata
# ---------------------------------------------------------------


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
