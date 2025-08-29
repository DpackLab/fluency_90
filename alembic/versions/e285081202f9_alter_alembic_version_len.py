"""Aumenta el tamaño de alembic_version.version_num para permitir IDs > 32."""

from alembic import op
import sqlalchemy as sa

# usa un id corto (<=32). Este es un ejemplo válido:
revision = "e285081202f9"
down_revision = "1ed087ba7b11"
branch_labels = None
depends_on = None


def upgrade():
    # En PostgreSQL, cambiar VARCHAR(32) -> VARCHAR(255) funciona incluso si es PK
    op.alter_column(
        "alembic_version",
        "version_num",
        existing_type=sa.String(length=32),
        type_=sa.String(length=255),
        existing_nullable=False,
        nullable=False,
    )


def downgrade():
    # Nota: podría fallar si hay un id > 32 ya guardado (caso de downgrade)
    op.alter_column(
        "alembic_version",
        "version_num",
        existing_type=sa.String(length=255),
        type_=sa.String(length=32),
        existing_nullable=False,
        nullable=False,
    )
