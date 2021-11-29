from server.configuration.db import AsyncSession
from server.configuration.exceptions import TagNotFoundException
from server.models.tipo_tag_model import TipoDeTagModel
from sqlalchemy.orm import selectinload
from typing import List, Optional
from server.configuration.environment import Environment
from sqlalchemy import select, insert, literal_column, delete, update


class TipoTagRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_tipo_tag(self, tipo_tag_dict: dict) -> TipoDeTagModel:
        """
        Método que faz a query para inserir um projeto no banco de dados de projetos
        Args:
            tipo_tag_dict: dicionário contendo os atributos do projeto

        Returns:
            Projeto criado
        """
        stmt = (
            insert(TipoDeTagModel).
            returning(literal_column('*')).
            values(**tipo_tag_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return TipoDeTagModel(**row_to_dict)

    async def atualiza_tipo_tag(self, tipo_tag_dict: dict) -> TipoDeTagModel:
        """
        Método que faz a query para atualizar um tipo de tag no banco de dados
        Args:
            tipo_tag_dict: dicionário contendo os atributos do tipo de tag

        Returns:
            Tipo de tag atualizado
        """
        new_user_entity = TipoDeTagModel(**tipo_tag_dict)
        self.db_session.add(new_user_entity)
        await self.db_session.flush()
        return new_user_entity

    async def find_tipos_tag_by_filtros(self, filtros: List) -> List[TipoDeTagModel]:
        """
        Método que faz a query para pegar tipos de tags por filtros no banco de dados
        Args:
            filtros: lista de ids de tipos de tags

        Returns:
            Lista com tipos de tags
        """
        stmt = (
            select(TipoDeTagModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_tipo_tag_by_filtros(self, filtros: List):
        """
        Método que faz a query para deletar tipos de tags por filtros no banco de dados
        Args:
            filtros: lista de ids de tipos de tags

        Returns:
            Nada
        """
        stmt = (
            delete(TipoDeTagModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)

    async def update_tipo_tag_by_guid(self, guid, projeto_update_dict: dict) -> TipoDeTagModel:
        """
        Método que faz a query para atualizar um tipo de tag pelo guid no banco de dados
        Args:
            guid: guid do projeto
            projeto_update_dict: dicionário contendo os atributos do projeto

        Returns:
            Projeto atualizado
        """
        stmt = (
            update(TipoDeTagModel).
            returning(literal_column('*')).
            where(TipoDeTagModel.guid == guid).
            values(**projeto_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise TagNotFoundException()
        row_to_dict = dict(query.fetchone())
        return TipoDeTagModel(**row_to_dict)
