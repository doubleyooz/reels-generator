"""Remove audio and images properties from reels

Revision ID: a4782fbd032a
Revises: 10d3f6959b4a
Create Date: 2025-07-28 13:39:11.899174
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision: str = 'a4782fbd032a'
down_revision: Union[str, Sequence[str], None] = '10d3f6959b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Drop the audio and images columns from the reels table
    op.drop_column('reels', 'audio')
    op.drop_column('reels', 'images')

def downgrade() -> None:
    """Downgrade schema."""
    # Add back the audio and images columns to the reels table
    op.add_column('reels', sa.Column('audio', sa.String, nullable=False, server_default=''))
    op.add_column('reels', sa.Column('images', ARRAY(sa.String), nullable=False, server_default='{}'))