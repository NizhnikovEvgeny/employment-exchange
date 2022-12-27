"""empty message

Revision ID: 4c88bf4899f3
Revises: 2f4b002133c4
Create Date: 2022-12-27 12:09:24.222780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c88bf4899f3'
down_revision = '2f4b002133c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('unique_user_job_respond', 'responds', [
                                'job_id', 'user_id'])


def downgrade() -> None:
    pass
