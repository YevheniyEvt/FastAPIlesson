"""add last columns to post table

Revision ID: 9c7a88067574
Revises: d17fb4bbae65
Create Date: 2025-01-19 12:16:34.342480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c7a88067574'
down_revision: Union[str, None] = 'd17fb4bbae65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',
                  sa.Column('published', sa.Boolean(),nullable=False, server_default='TRUE'))
    op.add_column('post',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'crated_at')
    pass
