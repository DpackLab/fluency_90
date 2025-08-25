from alembic import op
import sqlalchemy as sa

revision = "20250812_01_add_descripcion_idiomas"   # deja tu ID
down_revision = None                                # o el que tengas
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
