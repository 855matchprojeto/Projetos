from server.configuration.db import AsyncSession
from server.configuration.exceptions import EntidadeExternaNotFoundException
from server.models.interesse_model import InteresseModel
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment


class InteresseRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_interesse(self, interesse_dict: dict) -> InteresseModel:
        """
        Método que faz a query para inserir um interesse no banco de dados
        Args:
            interesse_dict: dicionário contendo os atributos do interesse

        Returns:
            interesse criado
        """
        stmt = (
            insert(InteresseModel).
                returning(literal_column('*')).
                values(**interesse_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return InteresseModel(**row_to_dict)

    async def atualiza_interesse(self, interesse_dict: dict) -> InteresseModel:
        """
        Método que faz a query para atualizar um interesse no banco de dados
        Args:
            interesse_dict: dicionário contendo os atributos do interesse

        Returns:
            interesse atualizado
        """
        curs_entity = InteresseModel(**interesse_dict)
        self.db_session.add(curs_entity)
        await self.db_session.flush()
        return curs_entity

    async def update_interesse_by_guid(self, guid, interesse_update_dict: dict) -> InteresseModel:
        """
        Método que faz a query para atualizar um interesse pelo guid no banco de dados
        Args:
            guid: guid do interesse
            interesse_update_dict: dicionário contendo os atributos do interesse

        Returns:
            interesse atualizado
        """
        stmt = (
            update(InteresseModel).
            returning(literal_column('*')).
            where(InteresseModel.guid == guid).
            values(**interesse_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise EntidadeExternaNotFoundException()
        row_to_dict = dict(query.fetchone())
        return InteresseModel(**row_to_dict)

    async def find_interesse_by_filtros(self, filtros: List) -> List[InteresseModel]:
        """
        Método que faz a query para pegar interesses por filtros no banco de dados
        Args:
            filtros: lista de ids de interesse

        Returns:
            Lista com interesses
        """
        stmt = (
            select(InteresseModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_interesse_by_filtros(self, filtros: List):
        """
        Método que faz a query para deletar interesse por filtros no banco de dados
        Args:
            filtros: lista de ids de interesse

        Returns:
            Nada
        """
        stmt = (
            delete(InteresseModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
