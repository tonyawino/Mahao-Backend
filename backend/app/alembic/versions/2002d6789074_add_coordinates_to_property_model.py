"""Add coordinates to property model

Revision ID: 2002d6789074
Revises: 180e7ada8c15
Create Date: 2022-01-05 07:49:55.578466

"""
from alembic import op
import sqlalchemy as sa
from app.models.easy_geometry import EasyGeometry

# revision identifiers, used by Alembic.
revision = '2002d6789074'
down_revision = '180e7ada8c15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('location', EasyGeometry(), nullable=False))
    op.create_index(op.f('ix_property_location'), 'property', ['location'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_property_location'), table_name='property')
    op.drop_column('property', 'location')
    # ### end Alembic commands ###
