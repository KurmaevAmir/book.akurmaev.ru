"""добавление столбца аватарки пользователя и столбца забронированных книг

Revision ID: 4947a4a0a1b0
Revises: 0c7b57f5d362
Create Date: 2022-04-27 20:29:04.380543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4947a4a0a1b0'
down_revision = '0c7b57f5d362'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('booking', sa.String(), nullable=True))
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=True))
    op.add_column('users', sa.Column('shopping_cart', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'shopping_cart')
    op.drop_column('users', 'avatar')
    op.drop_column('users', 'booking')
    # ### end Alembic commands ###
