"""stub: reintroduce 4544ef68328e en la cadena (sin cambios)"""

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# IDs de Alembic
revision = "4544ef68328e"
down_revision = "base_idiomas"  # este es el root que muestran tus logs
branch_labels = None
depends_on = None


def upgrade() -> None:
    # No hacemos nada: sólo “cosemos” la cadena
    pass


def downgrade() -> None:
    # Igual: no hacemos nada
    pass
