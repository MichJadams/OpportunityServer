"""create user table

Revision ID: beeacf726dbc
Revises: 
Create Date: 2023-04-05 09:38:48.390934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beeacf726dbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(50), nullable=False, unique=True),
                    sa.Column('hashed_password', sa.Unicode(225), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('users')
