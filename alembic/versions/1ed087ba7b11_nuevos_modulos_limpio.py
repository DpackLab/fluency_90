"""nuevos modulos (limpio)"""

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# revision identifiers, used by Alembic.
revision = "1ed087ba7b11"
down_revision = "4544ef68328e"  # <- debe apuntar al stub anterior
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Esta migración puede quedar vacía si solo la necesitas para “coser” la cadena
    # y los cambios reales ya están representados en el estado del modelo actual.
    pass


def downgrade() -> None:
    pass
