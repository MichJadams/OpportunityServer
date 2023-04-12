"""create the opportunity table

Revision ID: 3506c10b6f86
Revises: beeacf726dbc
Create Date: 2023-04-05 17:37:10.153771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3506c10b6f86'
down_revision = 'beeacf726dbc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    application_status_enum = sa.Enum('applied', 'interviewing', 'rejected', 'going_to_apply', 'partial_application', name='application_status')
    op.create_table('opportunities',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('url', sa.String(255)),
                    sa.Column('role_description', sa.String(255)),
                    sa.Column('notes', sa.String(1024)),
                    sa.Column('title', sa.String(255)),
                    sa.Column('date_applied', sa.DateTime),
                    sa.Column('application_status', application_status_enum, nullable=False),
                    sa.Column('user_name', sa.String(100),  sa.ForeignKey('users.name')),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
                    )


def downgrade() -> None:
    op.drop_table('opportunities')
    sa.Enum(name='application_status').drop(op.get_bind(), checkfirst=False)
