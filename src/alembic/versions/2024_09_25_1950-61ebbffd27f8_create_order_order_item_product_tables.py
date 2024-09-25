"""Create order, order_item, product tables

Revision ID: 61ebbffd27f8
Revises: 
Create Date: 2024-09-25 19:50:56.699565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '61ebbffd27f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('status', sa.Enum('during', 'sent', 'delivered', name='statusenum'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('orderitems',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.SmallInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orderitems')
    op.drop_table('products')
    op.drop_table('orders')
    # ### end Alembic commands ###