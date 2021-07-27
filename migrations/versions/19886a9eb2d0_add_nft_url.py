"""add nft url

Revision ID: 19886a9eb2d0
Revises: f570ad27301b
Create Date: 2021-07-26 10:55:05.702600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19886a9eb2d0'
down_revision = 'f570ad27301b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('NFT', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gateway_token_url', sa.String(length=700), nullable=True))
        batch_op.add_column(sa.Column('token_url', sa.String(length=700), nullable=True))
        batch_op.create_index(batch_op.f('ix_NFT_gateway_token_url'), ['gateway_token_url'], unique=False)
        batch_op.create_index(batch_op.f('ix_NFT_token_url'), ['token_url'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('NFT', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_NFT_token_url'))
        batch_op.drop_index(batch_op.f('ix_NFT_gateway_token_url'))
        batch_op.drop_column('token_url')
        batch_op.drop_column('gateway_token_url')

    # ### end Alembic commands ###
