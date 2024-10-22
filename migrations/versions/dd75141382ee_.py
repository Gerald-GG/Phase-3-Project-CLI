"""empty message

Revision ID: dd75141382ee
Revises: 
Create Date: 2023-12-14 21:50:07.585631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd75141382ee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('passwords', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'passwords', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'passwords', type_='foreignkey')
    op.drop_column('passwords', 'category_id')
    # ### end Alembic commands ###
