"""empty message

Revision ID: df46ba972287
Revises: a5947ca03a14
Create Date: 2021-11-28 22:07:07.318093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df46ba972287'
down_revision = 'a5947ca03a14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tb_rel_projeto_user_guid_user_key', 'tb_rel_projeto_user', type_='unique')
    op.create_unique_constraint(None, 'tb_rel_projeto_user', ['guid_user', 'id_projetos', 'id_funcao'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tb_rel_projeto_user', type_='unique')
    op.create_unique_constraint('tb_rel_projeto_user_guid_user_key', 'tb_rel_projeto_user', ['guid_user'])
    # ### end Alembic commands ###
