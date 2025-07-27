"""Users and reels use id as int

Revision ID: abc
Revises: 
Create Date: 2025-07-25 08:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

revision = 'abc'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False)
    )
    op.create_table(
        'reels',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('file', sa.String, nullable=False),
        sa.Column('audio', sa.String, nullable=False),
        sa.Column('images', ARRAY(sa.String), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('reels')
    op.drop_table('users')