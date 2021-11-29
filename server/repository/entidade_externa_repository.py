from server.configuration.db import AsyncSession
from server.configuration.exceptions import EntidadeExternaNotFoundException
from server.models.entidade_externa_model import EntidadeExternaModel
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment


class EntidadeExternaRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_entidade_externa(self, entidade_externa_dict: dict) -> EntidadeExternaModel:
        """
        Método que faz a query para inserir uma entidade externa no banco de dados
        Args:
            entidade_externa_dict: dicionário contendo os atributos da entidade externa

        Returns:
            Entidade externa criada
        """
        stmt = (
            insert(EntidadeExternaModel).
                returning(literal_column('*')).
                values(**entidade_externa_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return EntidadeExternaModel(**row_to_dict)

    async def atualiza_entidade_externa(self, entidade_externa_dict: dict) -> EntidadeExternaModel:
        """
        Método que faz a query para atualizar uma entidade externa no banco de dados
        Args:
            entidade_externa_dict: dicionário contendo os atributos da entidade externa

        Returns:
            Entidade externa atualizada
        """
        entidade_externa_entity = EntidadeExternaModel(**entidade_externa_dict)
        self.db_session.add(entidade_externa_entity)
        await self.db_session.flush()
        return entidade_externa_entity

    async def update_entidade_externa_by_guid(self, guid, entidade_externa_update_dict: dict) -> EntidadeExternaModel:
        """
        Método que faz a query para atualizar uma entidade externa pelo guid no banco de dados
        Args:
            guid: guid da entidade externa
            entidade_externa_update_dict: dicionário contendo os atributos da entidade externa

        Returns:
            Entidade externa atualizada
        """
        stmt = (
            update(EntidadeExternaModel).
            returning(literal_column('*')).
            where(EntidadeExternaModel.guid == guid).
            values(**entidade_externa_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise EntidadeExternaNotFoundException()
        row_to_dict = dict(query.fetchone())
        return EntidadeExternaModel(**row_to_dict)

    async def find_entidade_externas_by_filtros(self, filtros: List) -> List[EntidadeExternaModel]:
        """
        Método que faz a query para pegar entidades externas por filtros no banco de dados
        Args:
            filtros: lista de ids de entidades externas

        Returns:
            Lista com entidades externas
        """
        stmt = (
            select(EntidadeExternaModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_entidade_externa_by_filtros(self, filtros: List):
        """
        Método que faz a query para deletar entidades externas por filtros no banco de dados
        Args:
            filtros: lista de ids de entidades externas

        Returns:
            Nada
        """
        stmt = (
            delete(EntidadeExternaModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
