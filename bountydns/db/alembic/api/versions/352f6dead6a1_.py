"""empty message

Revision ID: 352f6dead6a1
Revises: 88f825143aa2
Create Date: 2019-03-25 02:07:05.127864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '352f6dead6a1'
down_revision = '88f825143aa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('mfa_secret', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'mfa_secret')
    op.drop_column('users', 'email_verified')
    # ### end Alembic commands ###
