"""add-zodiac-sign-description

Revision ID: 073f6ff3d5b4
Revises: 8a83a646d265
Create Date: 2021-03-22 09:47:07.894222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '073f6ff3d5b4'
down_revision = '8a83a646d265'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('zodiacs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('zodiacs', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###