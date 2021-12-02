from server.configuration.db import AsyncSession
from server.configuration.exceptions import EntidadeExternaNotFoundException
from server.models.curso_model import CursoModel
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment


class CursoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_curso(self, curso_dict: dict) -> CursoModel:
        """
        Método que faz a query para inserir um curso no banco de dados
        Args:
            curso_dict: dicionário contendo os atributos do curso

        Returns:
            curso criado
        """
        stmt = (
            insert(CursoModel).
                returning(literal_column('*')).
                values(**curso_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return CursoModel(**row_to_dict)

    async def atualiza_curso(self, curso_dict: dict) -> CursoModel:
        """
        Método que faz a query para atualizar um curso no banco de dados
        Args:
            curso_dict: dicionário contendo os atributos do curso

        Returns:
            Curso atualizado
        """
        curs_entity = CursoModel(**curso_dict)
        self.db_session.add(curs_entity)
        await self.db_session.flush()
        return curs_entity

    async def update_curso_by_guid(self, guid, curso_update_dict: dict) -> CursoModel:
        """
        Método que faz a query para atualizar um curso pelo guid no banco de dados
        Args:
            guid: guid do curso
            curso_update_dict: dicionário contendo os atributos do curso

        Returns:
            Curso atualizado
        """
        stmt = (
            update(CursoModel).
            returning(literal_column('*')).
            where(CursoModel.guid == guid).
            values(**curso_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise EntidadeExternaNotFoundException()
        row_to_dict = dict(query.fetchone())
        return CursoModel(**row_to_dict)

    async def find_curso_by_filtros(self, filtros: List) -> List[CursoModel]:
        """
        Método que faz a query para pegar cursos por filtros no banco de dados
        Args:
            filtros: lista de ids de curso

        Returns:
            Lista com Cursos
        """
        stmt = (
            select(CursoModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_curso_by_filtros(self, filtros: List):
        """
        Método que faz a query para deletar curso por filtros no banco de dados
        Args:
            filtros: lista de ids de curso

        Returns:
            Nada
        """
        stmt = (
            delete(CursoModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
