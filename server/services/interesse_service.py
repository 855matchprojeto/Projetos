from typing import Optional
from server.configuration.environment import Environment
from server.repository.interesse_repository import InteresseRepository
from server.models.interesse_model import InteresseModel
from sqlalchemy import or_, and_


class InteresseService():

    def __init__(self, interesse_repo: Optional[InteresseRepository] = None, environment: Optional[Environment] = None):
        self.interesse_repo = interesse_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        """
        Método que faz a lógica de pegar os interesses
        Args:
            id: id do interesse
            guid: guid do interesse

        Returns:
            Lista com interesses
        """
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    InteresseModel.id == id,
                    InteresseModel.guid == guid
                )]
        return await self.interesse_repo.find_interesse_by_filtros(filtros=filtros)

    async def create(self, interesse_input):
        """
        Método que faz a lógica de criar um interesse
        Args:
            interesse_input: interesse a ser criado

        Returns:
            interesse criado
        """
        interesse_dict = interesse_input.convert_to_dict()
        # Insere no banco de dados e retorna o interesse

        teste = await self.interesse_repo.insere_interesse(interesse_dict)
        return teste

    async def update(self, interesse_input):
        """
        Método que faz a lógica de atualizar um interesse
        Args:
            interesse_input: interesse a ser atualizado

        Returns:
            interesse atualizado
        """
        interesse_dict = interesse_input.convert_to_dict()
        # Insere no banco de dados e retorna o interesse
        return await self.interesse_repo.atualiza_interesse(interesse_dict)

    async def update_by_guid(self, guid, interesse_input):
        """
        Método que faz a lógica de atualizar um interesse pelo guid
        Args:
            guid: guid do interesse
            interesse_input: interesse externa a ser atualizada

        Returns:
            interesse atualizado
        """
        novo_interesse_dict = interesse_input.convert_to_dict()
        # Insere no banco de dados e retorna o interesse
        return await self.interesse_repo.update_interesse_by_guid(guid, novo_interesse_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar um interesse pelo guid
        Args:
            guid: guid do interesse

        Returns:
            Nada
        """
        return await self.interesse_repo.delete_interesse_by_filtros(filtros=[InteresseModel.guid == guid])

