"""3 Добавление новый столбцов: издательство, год издания, количество страниц

Revision ID: 2ef03d5aea93
Revises: 35fcf036d1ce
Create Date: 2022-07-01 18:13:29.949076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ef03d5aea93'
down_revision = '35fcf036d1ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('publishing_house', sa.String(), nullable=True))
    op.add_column('books', sa.Column('year_publishing', sa.DateTime(), nullable=True))
    op.add_column('books', sa.Column('number_of_pages', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'number_of_pages')
    op.drop_column('books', 'year_publishing')
    op.drop_column('books', 'publishing_house')
    # ### end Alembic commands ###
