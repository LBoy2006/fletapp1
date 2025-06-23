"""add categories to find

Revision ID: aa2d3456b789
Revises: e7d7ecc8e6d2
Create Date: 2025-07-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'aa2d3456b789'
down_revision: Union[str, Sequence[str], None] = 'e7d7ecc8e6d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('finds', sa.Column('category1', sa.String(), nullable=True))
    op.add_column('finds', sa.Column('category2', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('finds', 'category2')
    op.drop_column('finds', 'category1')
