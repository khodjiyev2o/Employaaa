"""new

Revision ID: 8909800e29ed
Revises: 48081c66c21c
Create Date: 2022-10-25 00:22:11.434407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8909800e29ed'
down_revision = '48081c66c21c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('question', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'question')
    # ### end Alembic commands ###