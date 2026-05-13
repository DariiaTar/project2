"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('admin', 'user', 'guest', name='userrole'), default='user'),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Enum('tennis', 'football', 'pool', 'gym', 'other', name='locationcategory'), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('price_per_hour', sa.Float(), nullable=False),
        sa.Column('capacity', sa.Integer(), default=1),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        'location_images',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('location_id', sa.Integer(), sa.ForeignKey('locations.id'), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        'slots',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('location_id', sa.Integer(), sa.ForeignKey('locations.id'), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('available', 'booked', 'blocked', name='slotstatus'), default='available'),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('slot_id', sa.Integer(), sa.ForeignKey('slots.id'), nullable=False),
        sa.Column('status', sa.Enum('pending_payment', 'confirmed', 'cancelled', 'completed', name='bookingstatus'), default='pending_payment'),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('guest_name', sa.String(), nullable=True),
        sa.Column('guest_email', sa.String(), nullable=True),
        sa.Column('guest_phone', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('bookings')
    op.drop_table('slots')
    op.drop_table('location_images')
    op.drop_table('locations')
    op.drop_table('users')
