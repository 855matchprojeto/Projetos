from server.configuration.db import AsyncSession
from server.configuration.exceptions import FuncaoProjectNotFoundException
from server.models.funcao_projeto_model import FuncaoProjetoModel
from sqlalchemy.orm import selectinload
from typing import List, Optional
from server.configuration.environment import Environment
from sqlalchemy import select, insert, literal_column, delete, update


class FuncoesProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_funcao(self, funcao_dict: dict) -> FuncaoProjetoModel:
        """
        Método que faz a query para inserir uma função no banco de dados
        Args:
            funcao_dict: dicionário contendo os atributos da função

        Returns:
            Função criada
        """
        stmt = (
            insert(FuncaoProjetoModel).
            returning(literal_column('*')).
            values(**funcao_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return FuncaoProjetoModel(**row_to_dict)

    async def atualiza_funcao(self, funcao_dict: dict) -> FuncaoProjetoModel:
        """
        Método que faz a query para atualizar uma função no banco de dados
        Args:
            funcao_dict: dicionário contendo os atributos da função

        Returns:
            Função atualizada
        """
        new_user_entity = FuncaoProjetoModel(**funcao_dict)
        self.db_session.add(new_user_entity)
        await self.db_session.flush()
        return new_user_entity

    async def find_funcoes_by_filtros(self, filtros: List) -> List[FuncaoProjetoModel]:
        """
        Método que faz a query para pegar funções por filtros no banco de dados
        Args:
            filtros: lista de ids de funções

        Returns:
            Lista com funções
        """
        stmt = (
            select(FuncaoProjetoModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_funcoes_by_filtros(self, filtros: List):
        """
        Método que faz a query para deletar funções por filtros no banco de dados
        Args:
            filtros: lista de ids de funções

        Returns:
            Nada
        """
        stmt = (
            delete(FuncaoProjetoModel).
            where(*filtros)
        )
        query = await self.db_session.execute(stmt)

    async def update_funcao_by_guid(self, guid, projeto_update_dict: dict) -> FuncaoProjetoModel:
        """
        Método que faz a query para atualizar uma função pelo guid no banco de dados
        Args:
            guid: guid da função
            projeto_update_dict: dicionário contendo os atributos da função

        Returns:
            função atualizada
        """
        stmt = (
            update(FuncaoProjetoModel).
            returning(literal_column('*')).
            where(FuncaoProjetoModel.guid == guid).
            values(**projeto_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise FuncaoProjectNotFoundException()
        row_to_dict = dict(query.fetchone())
        return FuncaoProjetoModel(**row_to_dict)