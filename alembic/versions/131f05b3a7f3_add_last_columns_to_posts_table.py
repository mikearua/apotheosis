"""add_last_columns_to_posts_table

Revision ID: 131f05b3a7f3
Revises: 65bac2073771
Create Date: 2026-10-01 15:49:23.667605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131f05b3a7f3'
down_revision: Union[str, Sequence[str], None] = '65bac2073771'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
