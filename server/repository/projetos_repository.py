from server.configuration.db import AsyncSession
from server.configuration.exceptions import ProjectNotFoundException
from server.models.entidade_externa_model import EntidadeExternaModel
from server.models.funcao_projeto_model import FuncaoProjetoModel
from server.models.projetos_model import ProjetosModel
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.relacao_projeto_entidade import RelacaoProjetoEntidadeModel
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel
from server.models.tag_model import TagModel


class ProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_projeto(self, projeto_dict: dict) -> ProjetosModel:
        stmt = (
            insert(ProjetosModel).
                returning(literal_column('*')).
                values(**projeto_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return ProjetosModel(**row_to_dict)

    async def atualiza_projeto(self, projeto_dict: dict) -> ProjetosModel:
        projeto_entity = ProjetosModel(**projeto_dict)
        self.db_session.add(projeto_entity)
        await self.db_session.flush()
        return projeto_entity

    async def update_projeto_by_guid(self, guid, projeto_update_dict: dict) -> ProjetosModel:
        stmt = (
            update(ProjetosModel).
            returning(literal_column('*')).
            where(ProjetosModel.guid == guid).
            values(**projeto_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise ProjectNotFoundException()
        row_to_dict = dict(query.fetchone())
        return ProjetosModel(**row_to_dict)

    async def find_projetos_by_filtros(self, filtros: List) -> List[ProjetosModel]:
        stmt = (
            select(ProjetosModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_projetos_by_filtros(self, filtros: List):
        stmt = (
            delete(ProjetosModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def find_projetos_by_ids(self) -> List[ProjetosModel]: #  project_ids: List[int]
        """
        SELECT proj.*, ent_ext.*, tag.*, proj_user.*, func_proj.*
        FROM tb_projetos proj
        INNER JOIN tb_rel_projeto_entidade proj_ent ON proj.id = proj_ent.id_projetos
        INNER JOIN tb_entidade_externa ent_ext ON proj_ent.id_entidade = ent_ext.id
        INNER JOIN tb_relacao_projeto_tag proj_tag ON proj.id = proj_tag.id_projetos
        INNER JOIN tb_tag tag ON proj_tag.id_tag = tb_tag.id
        INNER JOIN tb_rel_projeto_user proj_user ON proj.id = proj_user.id_projetos
        INNER JOIN tb_funcao_projeto func_proj ON proj_user.id_funcao = func_proj.id
        WHERE proj.id in :project_ids
        """
        stmt = (
            select(ProjetosModel)
            .distinct()
            .outerjoin(
                RelacaoProjetoEntidadeModel,
                RelacaoProjetoEntidadeModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                EntidadeExternaModel,
                RelacaoProjetoEntidadeModel.id_entidade == EntidadeExternaModel.id
            )
            .outerjoin(
                RelacaoProjetoTagModel,
                RelacaoProjetoTagModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                TagModel,
                RelacaoProjetoTagModel.id_tags == TagModel.id
            )
            .outerjoin(
                RelacaoProjetoUsuarioModel,
                RelacaoProjetoUsuarioModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                FuncaoProjetoModel,
                RelacaoProjetoUsuarioModel.id_funcao == FuncaoProjetoModel.id
            )
            .options(
                (
                    selectinload(ProjetosModel.rel_projeto_entidade).
                    selectinload(RelacaoProjetoEntidadeModel.projeto)
                ),
                (
                    selectinload(ProjetosModel.rel_projeto_tag).
                    selectinload(RelacaoProjetoTagModel.projeto)
                ),
                (
                    selectinload(ProjetosModel.rel_projeto_usuario).
                    selectinload(RelacaoProjetoUsuarioModel.projeto)
                )
            )

        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()


