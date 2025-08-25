"""merge heads

Revision ID: bb07faa338fb
Revises: 1ed087ba71b1, 20250812_03_content_metrics_roles
Create Date: 2025-08-12 12:48:16.743770

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "bb07faa338fb"
down_revision: Union[str, Sequence[str], None] = (
    "1ed087ba71b1",
    "20250812_03_content_metrics_roles",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
