from server.configuration.db import AsyncSession
from server.configuration.exceptions import ProjectNotFoundException
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.relacao_projeto_interesse import RelacaoProjetoInteresseModel


class RelacaoProjetoInteresseRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def find_rel_by_filtros(self, filtros: List) -> List[RelacaoProjetoInteresseModel]:

        stmt = (
            select(RelacaoProjetoInteresseModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def insere_relacao(self, relacao_dict: dict) -> RelacaoProjetoInteresseModel:
        stmt = (
            insert(RelacaoProjetoInteresseModel).
                returning(literal_column('*')).
                values(**relacao_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return RelacaoProjetoInteresseModel(**row_to_dict)


    async def delete_relacao_by_filtros(self, filtros: List):
        stmt = (
            delete(RelacaoProjetoInteresseModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
