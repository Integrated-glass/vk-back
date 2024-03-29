"""photo_volunteer

Revision ID: 7440551a6d7e
Revises: 7397864c53bb
Create Date: 2019-09-28 10:30:18.652410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7440551a6d7e'
down_revision = '7397864c53bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('volunteer_logins', sa.Column('photo', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('volunteer_logins', 'photo')
    # ### end Alembic commands ###
