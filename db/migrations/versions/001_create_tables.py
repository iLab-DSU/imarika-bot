"""create initial tables

Revision ID: 001
Revises: 
Create Date: 2025-03-18

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(255), unique=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('sender', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.func.now())
    )
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('level', sa.String(50), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('logs')
    op.drop_table('conversations')
    op.drop_table('users')
