"""ïnit

Revision ID: 32e49d01679a
Revises: 
Create Date: 2022-10-13 20:01:16.478653

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '32e49d01679a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('category', sa.String(45)),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_at', sa.DateTime(), default=datetime.datetime.now,
                  onupdate=datetime.datetime.now)
    )

    op.create_table(
        'user_role',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('role_id', sa.String(), sa.ForeignKey(
            "role.id"), nullable=False),
        sa.Column('permission_id', sa.Integer(), sa.ForeignKey(
            "permission.id"), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_at', sa.DateTime(), default=datetime.datetime.now,
                  onupdate=datetime.datetime.now)
    )

    op.create_table(
        'role',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('role', sa.String(45), unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_at', sa.DateTime(), default=datetime.datetime.now,
                  onupdate=datetime.datetime.now)
    )

    op.create_table(
        'permission',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('permission', sa.String(45), unique=True),
        sa.Column('permission_code', sa.String(45), unique=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_at', sa.DateTime(), default=datetime.datetime.now,
                  onupdate=datetime.datetime.now)
    )

    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('firstname', sa.String(45), nullable=False),
        sa.Column('lastname', sa.String(45), nullable=False),
        sa.Column('phone', sa.String(25), nullable=False, unique=True),
        sa.Column('email', sa.String(45), nullable=False, unique=True),
        sa.Column('password', sa.String(200), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_at', sa.DateTime(), default=datetime.datetime.now,
                  onupdate=datetime.datetime.now)
    )


def downgrade():
    op.drop_table('category')
    op.drop_table('user_role')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_table('user')
