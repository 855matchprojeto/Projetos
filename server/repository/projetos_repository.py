from server.configuration.db import AsyncSession
from server.configuration.exceptions import ProjectNotFoundException
from server.models.projetos_model import ProjetosModel
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment


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
