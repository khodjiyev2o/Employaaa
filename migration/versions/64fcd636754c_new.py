"""new

Revision ID: 64fcd636754c
Revises: ade2b2d462e3
Create Date: 2022-10-22 04:14:43.150123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64fcd636754c'
down_revision = 'ade2b2d462e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'members', 'companies', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'members', type_='foreignkey')
    op.drop_column('members', 'company_id')
    # ### end Alembic commands ###
