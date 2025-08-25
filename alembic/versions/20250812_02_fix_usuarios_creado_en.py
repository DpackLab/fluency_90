from alembic import op
import sqlalchemy as sa

revision = "20250812_02_fix_usuarios_creado_en"
down_revision = "1ed087ba71b1"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if insp.has_table("usuarios"):
        op.alter_column(
            "usuarios",
            "creado_en",
            existing_type=sa.DateTime(),
            type_=sa.DateTime(timezone=True),
            existing_nullable=False,
            server_default=sa.text("NOW()"),
        )


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if insp.has_table("usuarios"):
        op.alter_column(
            "usuarios",
            "creado_en",
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            existing_nullable=False,
            server_default=None,
        )
