"""Aumenta el tamaño de alembic_version.version_num para permitir IDs > 32."""

from alembic import op
import sqlalchemy as sa

revision = "e285081202f9"
down_revision = "1ed087ba7b11"  # <- la siguiente en la cadena
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ajusta a 64; si ya está en 64, esto es idempotente en Postgres.
    op.alter_column(
        "alembic_version",
        "version_num",
        type_=sa.String(length=64),
        existing_type=sa.String(length=32),
        existing_nullable=False,
    )


def downgrade() -> None:
    # Volver a 32 chars (solo si lo necesitas)
    op.alter_column(
        "alembic_version",
        "version_num",
        type_=sa.String(length=32),
        existing_type=sa.String(length=64),
        existing_nullable=False,
    )
