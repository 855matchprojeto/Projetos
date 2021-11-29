"""empty message

Revision ID: 4f154b560b09
Revises: df46ba972287
Create Date: 2021-11-28 22:17:33.452108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f154b560b09'
down_revision = 'df46ba972287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tb_historico_projeto_descricao_key', 'tb_historico_projeto', type_='unique')
    op.drop_constraint('tb_historico_projeto_titulo_key', 'tb_historico_projeto', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('tb_historico_projeto_titulo_key', 'tb_historico_projeto', ['titulo'])
    op.create_unique_constraint('tb_historico_projeto_descricao_key', 'tb_historico_projeto', ['descricao'])
    # ### end Alembic commands ###