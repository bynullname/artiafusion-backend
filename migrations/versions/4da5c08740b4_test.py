"""test

Revision ID: 4da5c08740b4
Revises: e62a2cceddfa
Create Date: 2023-07-14 15:00:08.552138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4da5c08740b4'
down_revision = 'e62a2cceddfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updateAt', sa.DateTime(), nullable=True))
        batch_op.drop_column('buttonMessageId')
        batch_op.drop_column('buttons')
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('buttons', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('buttonMessageId', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.drop_column('updateAt')

    # ### end Alembic commands ###