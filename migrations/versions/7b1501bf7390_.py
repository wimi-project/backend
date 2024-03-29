"""empty message

Revision ID: 7b1501bf7390
Revises: b6c3c9b60c69
Create Date: 2020-03-28 16:50:50.072673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b1501bf7390'
down_revision = 'b6c3c9b60c69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feedback', sa.Column('feedback_timestamp', sa.DateTime(), nullable=True))
    op.add_column('feedback', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'feedback', 'user', ['user_id'], ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'feedback', type_='foreignkey')
    op.drop_column('feedback', 'user_id')
    op.drop_column('feedback', 'feedback_timestamp')
    # ### end Alembic commands ###
