"""create tiempos_entrenamiento table"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1591d03b5ffe"
down_revision: Union[str, Sequence[str], None] = "20250812_03_content_metrics_roles"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tiempos_entrenamiento",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "usuario_id", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("fecha", sa.Date, nullable=False),
        sa.Column("minutos", sa.Integer, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )
    # Índice útil para consultas por usuario/fecha
    op.create_index(
        "ix_tiempos_entrenamiento_usuario_fecha",
        "tiempos_entrenamiento",
        ["usuario_id", "fecha"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_tiempos_entrenamiento_usuario_fecha",
        table_name="tiempos_entrenamiento",
    )
    op.drop_table("tiempos_entrenamiento")
