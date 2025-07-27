"""Change id from int to uuid for users and reels

Revision ID: 10d3f6959b4a
Revises: abc
Create Date: 2025-07-25 08:10:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '10d3f6959b4a'
down_revision = 'abc'
branch_labels = None
depends_on = None

def upgrade():
    # Check if id is already UUID to avoid errors
    users_columns = op.get_bind().execute(
        sa.text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'id'")
    ).fetchall()
    if not users_columns or users_columns[0][1] != 'uuid':
        # Add temporary UUID columns
        op.add_column('users', sa.Column('new_id', UUID(as_uuid=True), nullable=True))
        op.add_column('reels', sa.Column('new_id', UUID(as_uuid=True), nullable=True))
        op.add_column('reels', sa.Column('new_user_id', UUID(as_uuid=True), nullable=True))

        # Populate new_id with UUIDs for users
        op.execute("UPDATE users SET new_id = gen_random_uuid() WHERE new_id IS NULL")

        # Create a mapping table for old_id to new_id
        op.execute("""
            CREATE TEMPORARY TABLE user_id_mapping AS
            SELECT id AS old_id, new_id AS new_uuid FROM users
        """)

        # Populate new_id and new_user_id for reels
        op.execute("""
            UPDATE reels
            SET new_id = gen_random_uuid(),
                new_user_id = (SELECT new_uuid FROM user_id_mapping WHERE user_id_mapping.old_id = reels.user_id)
            WHERE new_id IS NULL
        """)

        # Drop constraints
        for constraint in ['reels_user_id_fkey', 'users_pkey', 'reels_pkey']:
            try:
                op.drop_constraint(constraint, 'reels' if 'reels' in constraint else 'users', type_='foreignkey' if 'fkey' in constraint else 'primary')
            except:
                pass

        # Drop old columns
        op.drop_column('users', 'id')
        op.drop_column('reels', 'id')
        op.drop_column('reels', 'user_id')

        # Rename new columns
        op.alter_column('users', 'new_id', new_column_name='id')
        op.alter_column('reels', 'new_id', new_column_name='id')
        op.alter_column('reels', 'new_user_id', new_column_name='user_id')

        # Recreate constraints
        op.create_primary_key('users_pkey', 'users', ['id'])
        op.create_primary_key('reels_pkey', 'reels', ['id'])
        op.create_foreign_key('reels_user_id_fkey', 'reels', 'users', ['user_id'], ['id'], ondelete='CASCADE')

        # Drop mapping table
        op.execute("DROP TABLE user_id_mapping")

def downgrade():
    # Add temporary INTEGER columns
    op.add_column('users', sa.Column('old_id', sa.Integer, nullable=True))
    op.add_column('reels', sa.Column('old_id', sa.Integer, nullable=True))
    op.add_column('reels', sa.Column('old_user_id', sa.Integer, nullable=True))

    # Create sequence for users if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'users_id_seq') THEN
                CREATE SEQUENCE users_id_seq;
            END IF;
        END $$;
    """)
    # Populate old_id for users
    op.execute("UPDATE users SET old_id = nextval('users_id_seq'::regclass) WHERE old_id IS NULL")

    # Create a mapping table for uuid to old_id
    op.execute("""
        CREATE TEMPORARY TABLE user_id_mapping AS
        SELECT id AS uuid, old_id AS old_int_id FROM users
    """)

    # Create sequence for reels if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'reels_id_seq') THEN
                CREATE SEQUENCE reels_id_seq;
            END IF;
        END $$;
    """)
    # Populate old_id and old_user_id for reels
    op.execute("""
        UPDATE reels
        SET old_id = nextval('reels_id_seq'::regclass),
            old_user_id = (SELECT old_int_id FROM user_id_mapping WHERE user_id_mapping.uuid = reels.user_id)
        WHERE old_id IS NULL
    """)

    # Drop constraints
    for constraint in ['reels_user_id_fkey', 'users_pkey', 'reels_pkey']:
        try:
            op.drop_constraint(constraint, 'reels' if 'reels' in constraint else 'users', type_='foreignkey' if 'fkey' in constraint else 'primary')
        except:
            pass

    # Drop UUID columns
    op.drop_column('users', 'id')
    op.drop_column('reels', 'id')
    op.drop_column('reels', 'user_id')

    # Rename old columns
    op.alter_column('users', 'old_id', new_column_name='id')
    op.alter_column('reels', 'old_id', new_column_name='id')
    op.alter_column('reels', 'old_user_id', new_column_name='user_id')

    # Recreate constraints
    op.create_primary_key('users_pkey', 'users', ['id'])
    op.create_primary_key('reels_pkey', 'reels', ['id'])
    op.create_foreign_key('reels_user_id_fkey', 'reels', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # Drop mapping table
    op.execute("DROP TABLE user_id_mapping")