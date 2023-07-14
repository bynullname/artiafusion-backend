"""test1

Revision ID: 21ef99437b35
Revises: 4da5c08740b4
Create Date: 2023-07-14 15:04:46.904761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21ef99437b35'
down_revision = '4da5c08740b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.create_index('idx_customer_id', ['customer_id'], unique=False)
        batch_op.create_index('idx_originating_message_id', ['originatingMessageId'], unique=False)
        batch_op.create_index(batch_op.f('ix_mj_customer_id'), ['customer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_mj_originatingMessageId'), ['originatingMessageId'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_mj_originatingMessageId'))
        batch_op.drop_index(batch_op.f('ix_mj_customer_id'))
        batch_op.drop_index('idx_originating_message_id')
        batch_op.drop_index('idx_customer_id')

    # ### end Alembic commands ###