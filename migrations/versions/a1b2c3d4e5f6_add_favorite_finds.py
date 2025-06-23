"""add favorite finds table

Revision ID: a1b2c3d4e5f6
Revises: aa2d3456b789
Create Date: 2025-07-21 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'aa2d3456b789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'favorite_finds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('find_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_favorite_finds_id'), 'favorite_finds', ['id'], unique=False)
    op.create_index(op.f('ix_favorite_finds_user_id'), 'favorite_finds', ['user_id'], unique=False)
    op.create_index(op.f('ix_favorite_finds_find_id'), 'favorite_finds', ['find_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_favorite_finds_find_id'), table_name='favorite_finds')
    op.drop_index(op.f('ix_favorite_finds_user_id'), table_name='favorite_finds')
    op.drop_index(op.f('ix_favorite_finds_id'), table_name='favorite_finds')
    op.drop_table('favorite_finds')
