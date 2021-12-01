from server.configuration.db import AsyncSession
from server.configuration.exceptions import ProjectNotFoundException
from server.models.entidade_externa_model import EntidadeExternaModel
from server.models.funcao_projeto_model import FuncaoProjetoModel
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from server.models.tag_model import TagModel


class RelacaoProjetoTagRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def find_rel_by_filtros(self, filtros: List) -> List[TagModel]:

        stmt = (
            select(RelacaoProjetoTagModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def insere_relacao(self, relacao_dict: dict) -> RelacaoProjetoTagModel:
        stmt = (
            insert(RelacaoProjetoTagModel).
                returning(literal_column('*')).
                values(**relacao_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return RelacaoProjetoTagModel(**row_to_dict)


    async def delete_relacao_by_filtros(self, filtros: List):
        stmt = (
            delete(RelacaoProjetoTagModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
