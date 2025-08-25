"""Auto: nuevos modulos (limpio)"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "1ed087ba71b1"
down_revision = "45441ef6823e"
branch_labels = None
depends_on = None


def upgrade():
    # Solo creamos 'retos'. Nada de DROP de tablas antiguas.
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if not insp.has_table("retos"):
        op.create_table(
            "retos",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("titulo", sa.String(length=100), nullable=False),
            sa.Column("descripcion", sa.Text, nullable=True),
            sa.Column("dificultad", sa.String(length=50), nullable=True),
            sa.Column("idioma_id", sa.Integer, sa.ForeignKey("idiomas.id"), nullable=False),
            sa.Column(
                "creado_en",
                sa.DateTime(timezone=True),
                server_default=sa.text("NOW()"),
                nullable=False,
            ),
        )
        # El índice sobre PK no es necesario, pero si lo quieres para simetría:
        op.create_index("ix_retos_id", "retos", ["id"], unique=False)


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if insp.has_table("retos"):
        # Elimina el índice si lo creaste arriba
        try:
            op.drop_index("ix_retos_id", table_name="retos")
        except Exception:
            pass
        op.drop_table("retos")
