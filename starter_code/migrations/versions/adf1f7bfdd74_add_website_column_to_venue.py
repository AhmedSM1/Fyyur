"""add website column to venue

Revision ID: adf1f7bfdd74
Revises: e98674c8ed17
Create Date: 2020-10-13 04:40:33.189574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adf1f7bfdd74'
down_revision = 'e98674c8ed17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('website', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    # ### end Alembic commands ###
