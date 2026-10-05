"""add_foreign_key_to_posts_table

Revision ID: 65bac2073771
Revises: acdce1fb079c
Create Date: 2026-10-01 15:15:55.051140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65bac2073771'
down_revision: Union[str, Sequence[str], None] = 'acdce1fb079c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_contraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
