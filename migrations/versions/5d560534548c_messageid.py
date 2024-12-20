"""messageId

Revision ID: 5d560534548c
Revises: c3eaa3aab857
Create Date: 2023-07-14 15:09:25.011467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d560534548c'
down_revision = 'c3eaa3aab857'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.add_column(sa.Column('MessageId', sa.String(length=255), nullable=True))
        batch_op.drop_index('idx_originating_message_id')
        batch_op.drop_index('ix_mj_originatingMessageId')
        batch_op.create_index('idx_message_id', ['MessageId'], unique=False)
        batch_op.create_index(batch_op.f('ix_mj_MessageId'), ['MessageId'], unique=False)
        batch_op.drop_column('originatingMessageId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mj', schema=None) as batch_op:
        batch_op.add_column(sa.Column('originatingMessageId', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.drop_index(batch_op.f('ix_mj_MessageId'))
        batch_op.drop_index('idx_message_id')
        batch_op.create_index('ix_mj_originatingMessageId', ['originatingMessageId'], unique=False)
        batch_op.create_index('idx_originating_message_id', ['originatingMessageId'], unique=False)
        batch_op.drop_column('MessageId')

    # ### end Alembic commands ###
