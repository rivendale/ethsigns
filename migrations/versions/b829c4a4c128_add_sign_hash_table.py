"""add-sign-hash-table

Revision ID: b829c4a4c128
Revises: cc5dce03ad39
Create Date: 2021-05-25 16:04:18.028626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b829c4a4c128'
down_revision = 'cc5dce03ad39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sign_hash',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('signhash', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sign_hash', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sign_hash_signhash'), ['signhash'], unique=True)

    op.create_table('user_sign_hashes',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('sign_hash', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sign_hash'], ['sign_hash.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['metamask_user.id'], )
    )
    op.drop_table('user_signs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_signs',
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('sign_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sign_id'], ['zodiacs.id'], name='user_signs_sign_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['metamask_user.id'], name='user_signs_user_id_fkey')
    )
    op.drop_table('user_sign_hashes')
    with op.batch_alter_table('sign_hash', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sign_hash_signhash'))

    op.drop_table('sign_hash')
    # ### end Alembic commands ###
