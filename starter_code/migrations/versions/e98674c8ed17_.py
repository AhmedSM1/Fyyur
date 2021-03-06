"""empty message

Revision ID: e98674c8ed17
Revises: 51b8b14152cd
Create Date: 2020-10-13 00:02:24.083065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e98674c8ed17'
down_revision = '51b8b14152cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('email', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'email')
    # ### end Alembic commands ###
