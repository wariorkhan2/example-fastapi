"""create posts table

Revision ID: a0479d303eed
Revises: 
Create Date: 2022-09-16 08:31:13.021546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0479d303eed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
