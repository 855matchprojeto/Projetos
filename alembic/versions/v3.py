"""empty message

Revision ID: 43cd0ceaf5f2
Revises: 23fff556207e
Create Date: 2021-10-18 22:11:46.729661

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '43cd0ceaf5f2'
down_revision = '23fff556207e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_projetos',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descricao'),
    sa.UniqueConstraint('guid'),
    sa.UniqueConstraint('titulo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_projetos')
    # ### end Alembic commands ###
