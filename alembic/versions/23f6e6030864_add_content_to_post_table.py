"""add content to post table

Revision ID: 23f6e6030864
Revises: 94690d2531df
Create Date: 2026-09-30 19:25:07.902417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23f6e6030864'
down_revision: Union[str, Sequence[str], None] = '94690d2531df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('data', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'data')
    pass
