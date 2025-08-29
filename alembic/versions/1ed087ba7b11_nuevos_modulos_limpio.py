"""nuevos modulos (limpio)

Revision ID: 1ed087ba7b11
Revises: 4544ef6832e8
Create Date: 2025-08-29 00:00:00
"""

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# revision identifiers, used by Alembic.
revision = "1ed087ba7b11"
down_revision = "4544ef6832e8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Esta migración puede quedar vacía si sólo la necesitas para “coser” la cadena
    # y los cambios reales ya están representados en el estado del modelo actual.
    pass


def downgrade() -> None:
    pass
