"""third

Revision ID: da84e5b2ef36
Revises: 44fc702bd403
Create Date: 2020-04-22 23:07:37.096006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da84e5b2ef36'
down_revision = '44fc702bd403'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('release_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'release_date')
    # ### end Alembic commands ###
