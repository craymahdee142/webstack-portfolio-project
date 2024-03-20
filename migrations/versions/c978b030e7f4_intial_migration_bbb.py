"""Intial migration bbb

Revision ID: c978b030e7f4
Revises: 
Create Date: 2024-03-13 13:40:53.737716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c978b030e7f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=70), nullable=False),
    sa.Column('mailing_address', sa.String(length=500), nullable=True),
    sa.Column('identify_proof', sa.String(length=70), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=70), nullable=False),
    sa.Column('filepath', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_num', sa.String(length=50), nullable=False),
    sa.Column('guest_id', sa.String(length=50), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=1020), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guest_id'),
    sa.UniqueConstraint('review_num')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_status', sa.String(length=80), nullable=False),
    sa.Column('price_per_night', sa.Float(), nullable=False),
    sa.Column('amenities', sa.String(length=80), nullable=False),
    sa.Column('additional_note', sa.String(length=255), nullable=True),
    sa.Column('floor_num', sa.Integer(), nullable=True),
    sa.Column('room_type_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['room_type_id'], ['room_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('floor_num')
    )
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reservation_num', sa.String(length=50), nullable=False),
    sa.Column('guest_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('room_num', sa.Integer(), nullable=False),
    sa.Column('check_in_date', sa.DateTime(), nullable=True),
    sa.Column('check_out_date', sa.DateTime(), nullable=True),
    sa.Column('num_of_adault', sa.Integer(), nullable=False),
    sa.Column('num_of_children', sa.Integer(), nullable=False),
    sa.Column('special_req', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['guest_id'], ['guest.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reservation_num'),
    sa.UniqueConstraint('room_num')
    )
    op.drop_table('reviews')
    op.drop_table('guests')
    op.drop_table('reservations')
    op.drop_table('rooms')
    op.drop_table('images')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('filename', sa.VARCHAR(length=70), nullable=False),
    sa.Column('filepath', sa.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rooms',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('room_num', sa.VARCHAR(length=70), nullable=False),
    sa.Column('room_status', sa.VARCHAR(length=80), nullable=False),
    sa.Column('price_per_night', sa.FLOAT(), nullable=False),
    sa.Column('amenities', sa.VARCHAR(length=80), nullable=False),
    sa.Column('additional_note', sa.VARCHAR(length=255), nullable=True),
    sa.Column('floor_num', sa.INTEGER(), nullable=True),
    sa.Column('room_type_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['room_type_id'], ['room_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('floor_num')
    )
    op.create_table('reservations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('reservation_num', sa.VARCHAR(length=50), nullable=False),
    sa.Column('guest_id', sa.INTEGER(), nullable=False),
    sa.Column('room_id', sa.INTEGER(), nullable=True),
    sa.Column('room_num', sa.INTEGER(), nullable=False),
    sa.Column('check_in_date', sa.DATETIME(), nullable=True),
    sa.Column('check_out_date', sa.DATETIME(), nullable=True),
    sa.Column('num_of_adault', sa.INTEGER(), nullable=False),
    sa.Column('num_of_children', sa.INTEGER(), nullable=False),
    sa.Column('special_req', sa.VARCHAR(length=255), nullable=True),
    sa.Column('status', sa.VARCHAR(length=100), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['guest_id'], ['guests.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reservation_num'),
    sa.UniqueConstraint('room_num')
    )
    op.create_table('guests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=250), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=70), nullable=False),
    sa.Column('mailing_address', sa.VARCHAR(length=500), nullable=True),
    sa.Column('identify_proof', sa.VARCHAR(length=70), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('reviews',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('review_num', sa.VARCHAR(length=50), nullable=False),
    sa.Column('guest_id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=False),
    sa.Column('comment', sa.VARCHAR(length=1020), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guest_id'),
    sa.UniqueConstraint('review_num')
    )
    op.drop_table('reservation')
    op.drop_table('room')
    op.drop_table('review')
    op.drop_table('image')
    op.drop_table('guest')
    # ### end Alembic commands ###
