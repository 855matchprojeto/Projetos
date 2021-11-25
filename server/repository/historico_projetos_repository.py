from server.configuration.db import AsyncSession
from server.models.entidade_externa_model import EntidadeExternaModel
from server.models.funcao_projeto_model import FuncaoProjetoModel
from server.models.historico_projeto_entidade import HistoricoProjetoEntidadeModel
from server.models.historico_projeto_tag import HistoricoProjetoTagModel
from server.models.historico_projetos_model import HistoricoProjetoModel
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.historico_projetos_usuarios_model import HistoricoProjetoUsuarioModel
from server.models.relacao_projeto_entidade import RelacaoProjetoEntidadeModel
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel
from server.models.tag_model import TagModel


class HistoricoProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_projeto(self, projeto_dict: dict) -> HistoricoProjetoModel:
        stmt = (
            insert(HistoricoProjetoModel).
            returning(literal_column('*')).
            values(**projeto_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return HistoricoProjetoModel(**row_to_dict)

    async def atualiza_projeto(self, projeto_dict: dict) -> HistoricoProjetoModel:
        new_user_entity = HistoricoProjetoModel(**projeto_dict)
        self.db_session.add(new_user_entity)
        await self.db_session.flush()
        return new_user_entity

    async def find_projetos_by_filtros(self, filtros: List) -> List[HistoricoProjetoModel]:
        stmt = (
            select(HistoricoProjetoModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_projetos_by_filtros(self, filtros: List):
        stmt = (
            delete(HistoricoProjetoModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def find_projetos_by_ids(self) -> List[HistoricoProjetoModel]: #  project_ids: List[int]
        stmt = (
            select(HistoricoProjetoModel)
            .distinct()
            .outerjoin(
                HistoricoProjetoEntidadeModel,
                HistoricoProjetoEntidadeModel.id_historico == HistoricoProjetoModel.id
            )
            .outerjoin(
                EntidadeExternaModel,
                HistoricoProjetoEntidadeModel.id_entidade == EntidadeExternaModel.id
            )
            .outerjoin(
                HistoricoProjetoTagModel,
                HistoricoProjetoTagModel.id_historico == HistoricoProjetoModel.id
            )
            .outerjoin(
                TagModel,
                HistoricoProjetoTagModel.id_tags == TagModel.id
            )
            # .outerjoin(
            #     HistoricoProjetoUsuarioModel,
            #     HistoricoProjetoUsuarioModel.id_historico == HistoricoProjetoModel.id
            # )
            # .outerjoin(
            #     FuncaoProjetoModel,
            #     HistoricoProjetoUsuarioModel.id_funcao == FuncaoProjetoModel.id
            # )
            .options(
                (
                    selectinload(HistoricoProjetoModel.historico_projeto_entidade).
                    selectinload(HistoricoProjetoEntidadeModel.entidade_externa)
            ),
                (
                    selectinload(HistoricoProjetoModel.historico_projeto_tag).
                    selectinload(HistoricoProjetoTagModel.tag)
            ),
            #     (
            #         selectinload(HistoricoProjetoModel.rel_historico_usuario).
            #         selectinload(HistoricoProjetoUsuarioModel.funcao)
            # )
            )

        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()


