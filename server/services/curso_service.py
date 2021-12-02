from typing import Optional
from server.configuration.environment import Environment
from server.repository.curso_repository import CursoRepository
from server.models.curso_model import CursoModel
from sqlalchemy import or_, and_


class CursoService():

    def __init__(self, curso_repo: Optional[CursoRepository] = None, environment: Optional[Environment] = None):
        self.curso_repo = curso_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        """
        Método que faz a lógica de pegar os cursos
        Args:
            id: id do curso
            guid: guid do curso

        Returns:
            Lista com cursos
        """
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    CursoModel.id == id,
                    CursoModel.guid == guid
                )]
        return await self.curso_repo.find_curso_by_filtros(filtros=filtros)

    async def create(self, curso_input):
        """
        Método que faz a lógica de criar um curso
        Args:
            curso_input: curso a ser criado

        Returns:
            Curso criado
        """
        curso_dict = curso_input.convert_to_dict()
        # Insere no banco de dados e retorna o curso

        teste = await self.curso_repo.insere_curso(curso_dict)
        return teste

    async def update(self, curso_input):
        """
        Método que faz a lógica de atualizar um curso
        Args:
            curso_input: curso a ser atualizado

        Returns:
            Curso atualizado
        """
        curso_dict = curso_input.convert_to_dict()
        # Insere no banco de dados e retorna o curso
        return await self.curso_repo.atualiza_curso(curso_dict)

    async def update_by_guid(self, guid, curso_input):
        """
        Método que faz a lógica de atualizar um curso pelo guid
        Args:
            guid: guid do curso
            curso_input: curso externa a ser atualizada

        Returns:
            Curso atualizado
        """
        novo_curso_dict = curso_input.convert_to_dict()
        # Insere no banco de dados e retorna o curso
        return await self.curso_repo.update_curso_by_guid(guid, novo_curso_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar um curso pelo guid
        Args:
            guid: guid do curso

        Returns:
            Nada
        """
        return await self.curso_repo.delete_curso_by_filtros(filtros=[CursoModel.guid == guid])

