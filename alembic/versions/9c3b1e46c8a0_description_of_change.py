"""description of change

Revision ID: 9c3b1e46c8a0
Revises: 
Create Date: 2024-09-26 21:57:25.366405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c3b1e46c8a0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transactions', 'categories', ['category_id'], ['category_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'category_id')
    # ### end Alembic commands ###
