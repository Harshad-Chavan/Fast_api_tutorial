"""add apt_num column

Revision ID: 5dce95934607
Revises: 8184b8b27f62
Create Date: 2023-07-05 21:15:09.491242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dce95934607'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
