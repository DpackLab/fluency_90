"""agregar columna descripcion manualmente"""
from alembic import op
import sqlalchemy as sa

# === REVISION INFO ===
revision = "45441ef6823e"
down_revision = "base_idiomas"   # <— aquí estaba el problema
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns("idiomas")]
    if "descripcion" not in cols:
        op.add_column("idiomas", sa.Column("descripcion", sa.String(), nullable=True))


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns("idiomas")]
    if "descripcion" in cols:
        op.drop_column("idiomas", "descripcion")
