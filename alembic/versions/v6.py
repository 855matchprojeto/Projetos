"""empty message

Revision ID: 45673177344e
Revises: 280e9621e69c
Create Date: 2021-11-02 18:02:11.775975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45673177344e'
down_revision = '280e9621e69c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tb_funcao_projeto_descricao_key', 'tb_funcao_projeto', type_='unique')
    op.drop_constraint('tb_funcao_projeto_nome_key', 'tb_funcao_projeto', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('tb_funcao_projeto_nome_key', 'tb_funcao_projeto', ['nome'])
    op.create_unique_constraint('tb_funcao_projeto_descricao_key', 'tb_funcao_projeto', ['descricao'])
    # ### end Alembic commands ###
