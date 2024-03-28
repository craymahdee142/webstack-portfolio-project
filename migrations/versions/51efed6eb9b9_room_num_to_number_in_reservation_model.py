""" Room num to number in reservation model

Revision ID: 51efed6eb9b9
Revises: 92b8ad645e4a
Create Date: 2024-03-17 23:00:21.690204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51efed6eb9b9'
down_revision = '92b8ad645e4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room_number', sa.Integer(), nullable=False))
        batch_op.create_unique_constraint('uq_reservation_room_number', ['room_number'])
        batch_op.drop_column('room_num')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room_num', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint('uq_reservation_room_number', type_='unique')
        batch_op.drop_column('room_number')

    # ### end Alembic commands ###