"""mint token model

Revision ID: e32e2d120eb6
Revises: b829c4a4c128
Create Date: 2021-06-16 11:31:32.679188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e32e2d120eb6'
down_revision = 'b829c4a4c128'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mint_sign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('transaction_hash', sa.String(length=500), nullable=True),
    sa.Column('mint_hash', sa.String(length=500), nullable=True),
    sa.Column('minted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('mint_sign', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_mint_sign_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_mint_sign_dob'), ['dob'], unique=False)
        batch_op.create_index(batch_op.f('ix_mint_sign_mint_hash'), ['mint_hash'], unique=False)
        batch_op.create_index(batch_op.f('ix_mint_sign_minted'), ['minted'], unique=False)
        batch_op.create_index(batch_op.f('ix_mint_sign_transaction_hash'), ['transaction_hash'], unique=False)

    op.create_table('user_transactions',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('mint_sign', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mint_sign'], ['mint_sign.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['metamask_user.id'], )
    )
    with op.batch_alter_table('day_sign', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('metamask_user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('month_sign', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('month',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

#     with op.batch_alter_table('sign', schema=None) as batch_op:
#         batch_op.alter_column('day',
#                existing_type=sa.BIGINT(),
#                type_=sa.Integer(),
#                existing_nullable=True)
#         batch_op.alter_column('id',
#                existing_type=sa.BIGINT(),
#                type_=sa.Integer(),
#                existing_nullable=False,
#                autoincrement=True)
#         batch_op.alter_column('month',
#                existing_type=sa.BIGINT(),
#                type_=sa.Integer(),
#                existing_nullable=True)
#         batch_op.alter_column('year',
#                existing_type=sa.BIGINT(),
#                type_=sa.Integer(),
#                existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('zodiacs', schema=None) as batch_op:
        batch_op.alter_column('base_index',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('zodiacs', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('base_index',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

#     with op.batch_alter_table('sign', schema=None) as batch_op:
#         batch_op.alter_column('year',
#                existing_type=sa.Integer(),
#                type_=sa.BIGINT(),
#                existing_nullable=True)
#         batch_op.alter_column('month',
#                existing_type=sa.Integer(),
#                type_=sa.BIGINT(),
#                existing_nullable=True)
#         batch_op.alter_column('id',
#                existing_type=sa.Integer(),
#                type_=sa.BIGINT(),
#                existing_nullable=False,
#                autoincrement=True)
#         batch_op.alter_column('day',
#                existing_type=sa.Integer(),
#                type_=sa.BIGINT(),
#                existing_nullable=True)

    with op.batch_alter_table('month_sign', schema=None) as batch_op:
        batch_op.alter_column('month',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('metamask_user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('day_sign', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    op.drop_table('user_transactions')
    with op.batch_alter_table('mint_sign', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_mint_sign_transaction_hash'))
        batch_op.drop_index(batch_op.f('ix_mint_sign_minted'))
        batch_op.drop_index(batch_op.f('ix_mint_sign_mint_hash'))
        batch_op.drop_index(batch_op.f('ix_mint_sign_dob'))
        batch_op.drop_index(batch_op.f('ix_mint_sign_created_at'))

    op.drop_table('mint_sign')
    # ### end Alembic commands ###
