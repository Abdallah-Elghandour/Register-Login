"""create user_token tabel

Revision ID: 634c5795f513
Revises: 5e78c120dc61
Create Date: 2024-09-30 15:40:21.790247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '634c5795f513'
down_revision: Union[str, None] = '5e78c120dc61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('access_key', sa.String(length=250), nullable=True),
    sa.Column('refresh_key', sa.String(length=250), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_tokens_access_key'), 'user_tokens', ['access_key'], unique=False)
    op.create_index(op.f('ix_user_tokens_refresh_key'), 'user_tokens', ['refresh_key'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_tokens_refresh_key'), table_name='user_tokens')
    op.drop_index(op.f('ix_user_tokens_access_key'), table_name='user_tokens')
    op.drop_table('user_tokens')
    # ### end Alembic commands ###
