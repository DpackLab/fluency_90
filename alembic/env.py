# --- INICIO BLOQUE SUGERIDO ---

import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Para que 'app' sea importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar .env si usas python-dotenv (opcional)
from dotenv import load_dotenv
load_dotenv()

# Config Alembic
config_alembic = context.config
if config_alembic.config_file_name is not None:
    fileConfig(config_alembic.config_file_name)

# Si prefieres URL desde .env
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config_alembic.set_main_option("sqlalchemy.url", DATABASE_URL)

# Importar Base y TODOS los modelos para poblar metadata
from app.database import Base

# IMPORTANTE: importa módulos que definen tablas
from app.models import (
    usuario, idioma, contenido, reto,                     # existentes
    contenido_diario, registro_sesion, ejercicio_resuelto, tiempo_entrenamiento,  # nuevos
    rol, usuario_rol
)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config_alembic.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config_alembic.get_section(config_alembic.config_ini_section),
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

# --- FIN BLOQUE SUGERIDO ---



