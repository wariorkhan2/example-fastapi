"""add foriegn key to posts table

Revision ID: 48ecc8c03d47
Revises: a2e8cc2d1fce
Create Date: 2022-09-16 09:29:55.651902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48ecc8c03d47'
down_revision = 'a2e8cc2d1fce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')

    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
