"""Add columns to user model

Revision ID: cf1f3e277acb
Revises: d4867f3a4c0a
Create Date: 2021-12-27 10:14:04.403033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf1f3e277acb'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('user', sa.Column('profile_picture', sa.String(), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(), nullable=True))
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=True))
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_user_full_name', table_name='user')
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=True)
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.create_index('ix_user_full_name', 'user', ['full_name'], unique=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'is_verified')
    op.drop_column('user', 'location')
    op.drop_column('user', 'profile_picture')
    op.drop_column('user', 'phone')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
