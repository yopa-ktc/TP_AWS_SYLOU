"""creation de la table leaderboard

Revision ID: bc78a692c5cb
Revises: 
Create Date: 2023-04-30 12:33:53.496279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc78a692c5cb'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('leaderboards',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('message', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('leaderboard')
