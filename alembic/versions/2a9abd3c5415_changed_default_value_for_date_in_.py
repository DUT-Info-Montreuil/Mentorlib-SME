"""Changed default value for date in comment

Revision ID: 2a9abd3c5415
Revises: 5c1b5ecc33fd
Create Date: 2024-05-12 17:13:58.762412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a9abd3c5415'
down_revision: Union[str, None] = '5c1b5ecc33fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###