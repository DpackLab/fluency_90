from alembic import op
import sqlalchemy as sa

revision = "20250812_03_content_metrics_roles"
down_revision = "20250812_02_fix_usuarios_creado_en"
branch_labels = None
depends_on = None


def upgrade():
    # contenidos
    op.create_table(
        "contenidos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("titulo", sa.String, nullable=False),
        sa.Column("tipo", sa.String, nullable=False),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("descripcion", sa.String, nullable=True),
        sa.Column("idioma_id", sa.Integer, sa.ForeignKey("idiomas.id"), nullable=False),
    )

    # contenidos_diarios
    op.create_table(
        "contenidos_diarios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fecha", sa.Date, nullable=False),
        sa.Column("idioma_id", sa.Integer, sa.ForeignKey("idiomas.id"), nullable=False),
        sa.Column(
            "contenido_id", sa.Integer, sa.ForeignKey("contenidos.id"), nullable=True
        ),
        sa.Column("objetivo_minutos", sa.Integer, nullable=True),
        sa.Column("notas", sa.String, nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    # registro_sesiones
    op.create_table(
        "registro_sesiones",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "usuario_id", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fin", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    # ejercicios_resueltos
    op.create_table(
        "ejercicios_resueltos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "usuario_id", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("reto_id", sa.Integer, sa.ForeignKey("retos.id"), nullable=True),
        sa.Column("tipo", sa.String, nullable=True),
        sa.Column("wpm", sa.Float, nullable=True),
        sa.Column("comprension_pct", sa.Float, nullable=True),
        sa.Column("errores_por_min", sa.Float, nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    # roles
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String, nullable=False, unique=True),
        sa.Column("descripcion", sa.String, nullable=True),
    )

    # usuario_rol
    op.create_table(
        "usuario_rol",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "usuario_id", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("rol_id", sa.Integer, sa.ForeignKey("roles.id"), nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    # retos: asegurar columnas nuevas si no existen
    with op.batch_alter_table("retos", schema=None) as batch_op:
        if not has_column("retos", "activo"):
            batch_op.add_column(
                sa.Column("activo", sa.Boolean, nullable=False, server_default="true")
            )
        if not has_column("retos", "creado_en"):
            batch_op.add_column(
                sa.Column(
                    "creado_en",
                    sa.DateTime(timezone=True),
                    server_default=sa.text("NOW()"),
                    nullable=False,
                )
            )


def downgrade():
    op.drop_table("usuario_rol")
    op.drop_table("roles")
    op.drop_table("ejercicios_resueltos")
    op.drop_table("registro_sesiones")
    op.drop_table("contenidos_diarios")
    op.drop_table("contenidos")
    # No bajamos cambios en "retos" por seguridad (evitar pérdida de datos). Quita si lo necesitas.


# Utilidad mínima para comprobar columna en batch_alter (no siempre disponible: depende del motor)
def has_column(table, column):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns(table)]
    return column in cols
