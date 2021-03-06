"""token table

Revision ID: 73ea12e8a3d0
Revises: 
Create Date: 2017-05-04 11:00:50.116338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73ea12e8a3d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=300), nullable=True),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_token')
    # ### end Alembic commands ###
