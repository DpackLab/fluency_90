"""stub: reintroduce 4544ef68328e en la cadena (sin cambios)"""

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# IDs de Alembic
revision = "4544ef68328e"
down_revision = None  # <- ESTE ES EL CAMBIO CLAVE
branch_labels = ("base_idiomas",)  # opcional: solo etiqueta de rama
depends_on = None


def upgrade() -> None:
    # No hacemos nada; es un stub para “coser” la cadena.
    pass


def downgrade() -> None:
    # Igual: no hacemos nada.
    pass
