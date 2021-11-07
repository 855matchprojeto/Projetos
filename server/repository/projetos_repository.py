from server.configuration.db import AsyncSession
from server.models.permissao_model import Permissao

from server.models.projetos_model import ProjetosModel
from server.models.entidade_externa_model import EntidadeExternaModel
from server.models.tag_model import TagModel
from server.models.funcao_projeto_model import FuncaoProjeto

from server.models.relacao_projeto_entidade import RelacaoProjetoEntidadeModel
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel

from sqlalchemy import select
from typing import List, Optional
from server.configuration.environment import Environment
from sqlalchemy.orm import selectinload
from sqlalchemy import and_

class ProjetosRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def find_projetos_by_ids(self, project_ids: List[int]) -> List[ProjetosModel]:
        '''
        SELECT proj.*, ent_ext.*, tag.*, proj_user.*, func_proj.* 
        FROM tb_projetos proj 
        INNER JOIN tb_rel_projeto_entidade proj_ent ON proj.id = proj_ent.id_projetos
        INNER JOIN tb_entidade_externa ent_ext ON proj_ent.id_entidade = ent_ext.id
        INNER JOIN tb_relacao_projeto_tag proj_tag ON proj.id = proj_tag.id_projetos
        INNER JOIN tb_tag tag ON proj_tag.id_tag = tb_tag.id
        INNER JOIN tb_rel_projeto_user proj_user ON proj.id = proj_user.id_projetos
        INNER JOIN tb_funcao_projeto func_proj ON proj_user.id_funcao = func_proj.id
        WHERE proj.id in :project_ids

        '''
        stmt = (
            select([ProjetosModel, EntidadeExternaModel, TagModel, FuncaoProjeto]).
            join(
                RelacaoProjetoEntidadeModel,
                RelacaoProjetoTagModel,
                RelacaoProjetoUsuarioModel,
                and_(
                    RelacaoProjetoEntidadeModel.id_projetos == ProjetosModel.id,
                    RelacaoProjetoEntidadeModel.id_entidade == EntidadeExternaModel.id,
                    RelacaoProjetoTagModel.id_projetos == ProjetosModel.id,
                    RelacaoProjetoTagModel.id_tags == TagModel.id,
                    RelacaoProjetoUsuarioModel.id_projetos == ProjetosModel.id,
                    RelacaoProjetoUsuarioModel.id_funcao == FuncaoProjeto.id,
                    ProjetosModel.id.in_(project_ids)
                )
            ).options(
                selectinload(Permissao.vinculos_permissao_funcao)
            )
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()



    async def get_all_projetos(self) -> List[ProjetosModel]:
        '''
        SELECT proj.*, ent_ext.*, tag.*, proj_user.*, func_proj.* 
        FROM tb_projetos proj 
        INNER JOIN tb_rel_projeto_entidade proj_ent ON proj.id = proj_ent.id_projetos
        INNER JOIN tb_entidade_externa ent_ext ON proj_ent.id_entidade = ent_ext.id
        INNER JOIN tb_relacao_projeto_tag proj_tag ON proj.id = proj_tag.id_projetos
        INNER JOIN tb_tag tag ON proj_tag.id_tag = tb_tag.id
        INNER JOIN tb_rel_projeto_user proj_user ON proj.id = proj_user.id_projetos
        INNER JOIN tb_funcao_projeto func_proj ON proj_user.id_funcao = func_proj.id

        '''
        stmt = (
            select([ProjetosModel, EntidadeExternaModel, TagModel, FuncaoProjeto]).
            join(
                RelacaoProjetoEntidadeModel,
                RelacaoProjetoTagModel,
                RelacaoProjetoUsuarioModel,
                and_(
                    RelacaoProjetoEntidadeModel.id_projetos == ProjetosModel.id,
                    RelacaoProjetoEntidadeModel.id_entidade == EntidadeExternaModel.id,
                    RelacaoProjetoTagModel.id_projetos == ProjetosModel.id,
                    RelacaoProjetoTagModel.id_tags == TagModel.id,
                    RelacaoProjetoUsuarioModel.id_projetos == ProjetosModel.id,
                    RelacaoProjetoUsuarioModel.id_funcao == FuncaoProjeto.id,
                )
            ).options(
                selectinload(Permissao.vinculos_permissao_funcao)
            )
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()
