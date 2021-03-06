"""Add __ts_vector__ column for full text search

Revision ID: 180e7ada8c15
Revises: 151032ac960f
Create Date: 2021-12-31 06:30:43.908772

"""
from alembic import op
import sqlalchemy as sa
from app.models.ts_vector import TSVector


# revision identifiers, used by Alembic.
revision = '180e7ada8c15'
down_revision = '151032ac960f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('__ts_vector__', TSVector(), sa.Computed("to_tsvector('english', title || ' ' || description || ' ' || location_name)", persisted=True), nullable=True))
    op.create_index('ix_property___ts_vector__', 'property', ['__ts_vector__'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_property___ts_vector__', table_name='property', postgresql_using='gin')
    op.drop_column('property', '__ts_vector__')
    # ### end Alembic commands ###
