"""add forein key to post table

Revision ID: d17fb4bbae65
Revises: cdb457c27fb5
Create Date: 2025-01-19 12:03:48.066515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd17fb4bbae65'
down_revision: Union[str, None] = 'cdb457c27fb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_user_fk', source_table='post', referent_table='user',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
