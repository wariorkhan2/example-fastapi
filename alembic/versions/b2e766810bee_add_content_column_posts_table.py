"""add content column posts table

Revision ID: b2e766810bee
Revises: a0479d303eed
Create Date: 2022-09-16 08:43:48.679829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2e766810bee'
down_revision = 'a0479d303eed'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
