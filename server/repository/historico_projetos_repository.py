from server.configuration.db import AsyncSession
from server.models.historico_projetos_model import HistoricoProjetoModel
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete
from typing import List, Optional
from server.configuration.environment import Environment


class ProjetoRepository:

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