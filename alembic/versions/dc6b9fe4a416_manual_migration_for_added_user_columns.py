"""Manual migration for added user columns

Revision ID: dc6b9fe4a416
Revises: <PREVIOUS_REVISION_ID> # This will be the actual previous revision ID from your alembic/versions/ folder
Create Date: 2025-07-17 04:17:05.123456 # Your specific timestamp will be here

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dc6b9fe4a416'
down_revision = None # Alembic will fill this with your previous head revision automatically
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'uuid' column to 'users' table
    # Model: nullable=False, unique=True. Using server_default for existing rows.
    #op.add_column('users', sa.Column('uuid', mysql.CHAR(length=36), nullable=False, unique=True, server_default=sa.text('UUID()')))
    #op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=True)


    # Add 'is_superuser' column to 'users' table
    # Model: nullable=False, default=False. Using server_default for existing rows.
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('0'))) # 0 for False


    # Add 'user_type_id' column to 'users' table
    # Model: nullable=False. Added as nullable=True for this migration to avoid breaking existing rows.
    # IMPORTANT: You MUST update existing user rows with a valid user_type_id AFTER this migration,
    # then run another migration to make this column nullable=False if needed.
    #op.add_column('users', sa.Column('user_type_id', mysql.CHAR(length=36), sa.ForeignKey('user_type_options.id'), nullable=True, index=True))
    # op.create_index(op.f('ix_users_user_type_id'), 'users', ['user_type_id'], unique=False)


    # Add 'referred_by_id' column to 'users' table
    # Model: nullable=True
    op.add_column('users', sa.Column('referred_by_id', mysql.CHAR(length=36), sa.ForeignKey('users.id'), nullable=True, index=True))
    op.create_index(op.f('ix_users_referred_by_id'), 'users', ['referred_by_id'], unique=False)


    # Add 'first_name' column to 'users' table
    # Model: nullable=True
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=True))


    # Add 'last_name' column to 'users' table
    # Model: nullable=True
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=True))


    # Add 'last_login_at' column to 'users' table
    # Model: nullable=True. Consider current_timestamp for server_default if desired.
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Drop columns in reverse order of addition
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')

    op.drop_index(op.f('ix_users_referred_by_id'), table_name='users')
    op.drop_column('users', 'referred_by_id')

    # op.drop_index(op.f('ix_users_user_type_id'), table_name='users')
    #op.drop_column('users', 'user_type_id')

    op.drop_column('users', 'is_superuser')

    #op.drop_index(op.f('ix_users_uuid'), table_name='users')
    #op.drop_column('users', 'uuid')