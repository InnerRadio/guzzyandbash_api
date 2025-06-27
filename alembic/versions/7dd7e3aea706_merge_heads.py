# Mako template for a new Alembic revision script

"""
Merge heads

Revision ID: 7dd7e3aea706
Revises: ('3af0b1d93aa3', '7654221ae037')
Create Date: 2025-06-25 10:08:55.110451

"""

# IMPORTS
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dd7e3aea706'
down_revision = ('3af0b1d93aa3', '7654221ae037')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass