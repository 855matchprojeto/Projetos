"""empty message

Revision ID: 258f7183a9fe
Revises: c00bae21a6e5
Create Date: 2021-11-24 20:56:06.785245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '258f7183a9fe'
down_revision = 'c00bae21a6e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_historico_projeto_tag', sa.Column('id_historico', sa.BigInteger(), nullable=True))
    op.drop_constraint('tb_historico_projeto_tag_id_projetos_fkey', 'tb_historico_projeto_tag', type_='foreignkey')
    op.create_foreign_key(None, 'tb_historico_projeto_tag', 'tb_historico_projeto', ['id_historico'], ['id'])
    op.drop_column('tb_historico_projeto_tag', 'id_projetos')
    op.add_column('tb_historico_projeto_usuario', sa.Column('id_historico', sa.BigInteger(), nullable=True))
    op.drop_constraint('tb_historico_projeto_usuario_id_projetos_fkey', 'tb_historico_projeto_usuario', type_='foreignkey')
    op.create_foreign_key(None, 'tb_historico_projeto_usuario', 'tb_historico_projeto', ['id_historico'], ['id'])
    op.drop_column('tb_historico_projeto_usuario', 'id_projetos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_historico_projeto_usuario', sa.Column('id_projetos', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tb_historico_projeto_usuario', type_='foreignkey')
    op.create_foreign_key('tb_historico_projeto_usuario_id_projetos_fkey', 'tb_historico_projeto_usuario', 'tb_projetos', ['id_projetos'], ['id'])
    op.drop_column('tb_historico_projeto_usuario', 'id_historico')
    op.add_column('tb_historico_projeto_tag', sa.Column('id_projetos', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tb_historico_projeto_tag', type_='foreignkey')
    op.create_foreign_key('tb_historico_projeto_tag_id_projetos_fkey', 'tb_historico_projeto_tag', 'tb_projetos', ['id_projetos'], ['id'])
    op.drop_column('tb_historico_projeto_tag', 'id_historico')
    # ### end Alembic commands ###
