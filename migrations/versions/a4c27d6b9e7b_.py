"""empty message

Revision ID: a4c27d6b9e7b
Revises: 5cf93249da4c
Create Date: 2017-11-05 16:44:00.676647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4c27d6b9e7b'
down_revision = '5cf93249da4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_room_access_request_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_room_access_request_time')
    # ### end Alembic commands ###
