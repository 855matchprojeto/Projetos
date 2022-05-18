"""empty message

Revision ID: 16682aadcd4c
Revises: 047f840b61f1
Create Date: 2022-05-02 21:11:19.549277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '16682aadcd4c'
down_revision = '047f840b61f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_arquivo',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('file_type', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guid')
    )
    op.add_column('tb_projetos', sa.Column('id_imagem_projeto', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'tb_projetos', 'tb_arquivo', ['id_imagem_projeto'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tb_projetos_id_imagem_projeto_fkey', 'tb_projetos', type_='foreignkey')
    op.drop_column('tb_projetos', 'id_imagem_projeto')
    op.drop_table('tb_arquivo')
    # ### end Alembic commands ###
