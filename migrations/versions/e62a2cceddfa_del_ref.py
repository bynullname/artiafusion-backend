"""del ref

Revision ID: e62a2cceddfa
Revises: 7be2be847da1
Create Date: 2023-07-14 14:52:47.802880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62a2cceddfa'
down_revision = '7be2be847da1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.drop_column('ref')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ref', sa.VARCHAR(length=255), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
