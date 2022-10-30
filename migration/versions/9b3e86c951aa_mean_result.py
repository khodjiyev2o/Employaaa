"""mean-result

Revision ID: 9b3e86c951aa
Revises: 2791d0979226
Create Date: 2022-10-28 11:18:43.307896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b3e86c951aa'
down_revision = '2791d0979226'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mean_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('num_of_qs', sa.Integer(), nullable=True),
    sa.Column('num_of_ans', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mean_results_id'), 'mean_results', ['id'], unique=True)
    op.add_column('users', sa.Column('mean_result', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'mean_result')
    op.drop_index(op.f('ix_mean_results_id'), table_name='mean_results')
    op.drop_table('mean_results')
    # ### end Alembic commands ###