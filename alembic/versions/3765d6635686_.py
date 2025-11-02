# Mako template for a new Alembic revision script

"""
empty message

Revision ID: 3765d6635686
Revises: ('7d8c38cf9261', 'dc6b9fe4a416')
Create Date: 2025-07-17 08:23:37.268192

"""

# IMPORTS
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3765d6635686'
down_revision = ('7d8c38cf9261', 'dc6b9fe4a416')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass