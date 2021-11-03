from server.configuration.db import AsyncSession
from server.configuration.exceptions import TagNotFoundException
from server.models.tag_model import TagModel
from sqlalchemy.orm import selectinload
from typing import List, Optional
from server.configuration.environment import Environment
from sqlalchemy import select, insert, literal_column, delete, update


class TagRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_tag(self, tag_dict: dict) -> TagModel:
        stmt = (
            insert(TagModel).
            returning(literal_column('*')).
            values(**tag_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return TagModel(**row_to_dict)

    async def atualiza_tag(self, tag_dict: dict) -> TagModel:
        new_user_entity = TagModel(**tag_dict)
        self.db_session.add(new_user_entity)
        await self.db_session.flush()
        return new_user_entity

    async def find_tags_by_filtros(self, filtros: List) -> List[TagModel]:
        stmt = (
            select(TagModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_tags_by_filtros(self, filtros: List):
        stmt = (
            delete(TagModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()


    async def update_tag_by_guid(self, guid, projeto_update_dict: dict) -> TagModel:
        stmt = (
            update(TagModel).
            returning(literal_column('*')).
            where(TagModel.guid == guid).
            values(**projeto_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise TagNotFoundException()
        row_to_dict = dict(query.fetchone())
        return TagModel(**row_to_dict)