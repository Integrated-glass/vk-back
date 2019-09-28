"""age restriction - event

Revision ID: d3d33e32795b
Revises: f7977c9fa185
Create Date: 2019-09-28 16:02:23.361823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3d33e32795b'
down_revision = 'f7977c9fa185'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('age_restriction', sa.Integer(), server_default='0', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'age_restriction')
    # ### end Alembic commands ###