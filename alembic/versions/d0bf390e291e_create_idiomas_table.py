"""create idiomas table (root)"""
from alembic import op
import sqlalchemy as sa

# === REVISION INFO ===
revision = "base_idiomas"   # <— ID corto y claro
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    has_table = insp.has_table("idiomas")
    cols = [c["name"] for c in insp.get_columns("idiomas")] if has_table else []

    if not has_table:
        op.create_table(
            "idiomas",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("nombre", sa.String, nullable=False, unique=True),
            sa.Column("codigo_iso", sa.String, nullable=False, unique=True),
        )
    else:
        # Refuerza columnas mínimas si venías de un estado raro
        if "nombre" not in cols:
            op.add_column("idiomas", sa.Column("nombre", sa.String, nullable=False))
        if "codigo_iso" not in cols:
            op.add_column("idiomas", sa.Column("codigo_iso", sa.String, nullable=False))


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if insp.has_table("idiomas"):
        op.drop_table("idiomas")
