"""metamaks user

Revision ID: 5cfcf5cca19e
Revises: 073f6ff3d5b4
Create Date: 2021-05-10 13:37:59.495314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cfcf5cca19e'
down_revision = '073f6ff3d5b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metamask_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('metamask_user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_metamask_user_address'), ['address'], unique=True)

    op.create_table('user_signs',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('sign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sign_id'], ['zodiacs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['metamask_user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_signs')
    with op.batch_alter_table('metamask_user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_metamask_user_address'))

    op.drop_table('metamask_user')
    # ### end Alembic commands ###