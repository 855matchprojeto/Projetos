from server.configuration.db import AsyncSession
from server.models.funcao_projeto_model import FuncaoProjeto
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete
from typing import List, Optional
from server.configuration.environment import Environment


class FuncoesProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_funcao(self, projeto_dict: dict) -> FuncaoProjeto:
        stmt = (
            insert(FuncaoProjeto).
            returning(literal_column('*')).
            values(**projeto_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return FuncaoProjeto(**row_to_dict)

    async def atualiza_funcao(self, projeto_dict: dict) -> FuncaoProjeto:
        new_user_entity = FuncaoProjeto(**projeto_dict)
        self.db_session.add(new_user_entity)
        await self.db_session.flush()
        return new_user_entity

    async def find_funcoes_by_filtros(self, filtros: List) -> List[FuncaoProjeto]:
        stmt = (
            select(FuncaoProjeto).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_funcoes_by_filtros(self, filtros: List):
        stmt = (
            delete(FuncaoProjeto).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()