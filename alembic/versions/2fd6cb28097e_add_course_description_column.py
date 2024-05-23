"""Add course description column

Revision ID: 2fd6cb28097e
Revises: 99b3210c8006
Create Date: 2024-05-06 17:18:50.463853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fd6cb28097e'
down_revision: Union[str, None] = '99b3210c8006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('description', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'description')
    # ### end Alembic commands ###