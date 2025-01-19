"""add content colum to post table

Revision ID: c552e6c92996
Revises: 74158159016e
Create Date: 2025-01-19 11:44:50.981414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c552e6c92996'
down_revision: Union[str, None] = '74158159016e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass
