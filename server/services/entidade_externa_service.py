from typing import Optional
from server.configuration.environment import Environment
from server.repository.entidade_externa_repository import EntidadeExternaRepository
from server.models.entidade_externa_model import EntidadeExternaModel
from sqlalchemy import or_, and_


class EntidadeExternaService():

    def __init__(self, entidade_externa_repo: Optional[EntidadeExternaRepository] = None, environment: Optional[Environment] = None):
        self.entidade_externa_repo = entidade_externa_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        """
        Método que faz a lógica de pegar as entidades externas
        Args:
            id: id da entidade externa
            guid: guid da entidade externa

        Returns:
            Lista com entidades externas
        """
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    EntidadeExternaModel.id == id,
                    EntidadeExternaModel.guid == guid
                )]
        return await self.entidade_externa_repo.find_entidade_externas_by_filtros(filtros=filtros)

    async def create(self, entidade_externa_input):
        """
        Método que faz a lógica de criar uma entidade externa
        Args:
            entidade_externa_input: entidade externa a ser criada

        Returns:
            Entidade externa criada
        """
        entidade_externa_dict = entidade_externa_input.convert_to_dict()
        # Insere no banco de dados e retorna a entidade externa

        teste = await self.entidade_externa_repo.insere_entidade_externa(entidade_externa_dict)
        return teste

    async def update(self, entidade_externa_input):
        """
        Método que faz a lógica de atualizar uma entidade externa
        Args:
            entidade_externa_input: entidade externa a ser atualizada

        Returns:
            Entidade externa atualizada
        """
        nova_entidade_externa_dict = entidade_externa_input.convert_to_dict()
        # Insere no banco de dados e retorna a entidade externa
        return await self.entidade_externa_repo.atualiza_entidade_externa(nova_entidade_externa_dict)

    async def update_by_guid(self, guid, entidade_externa_input):
        """
        Método que faz a lógica de atualizar uma entidade externa pelo guid
        Args:
            guid: guid da entidade externa
            entidade_externa_input: entidade externa a ser atualizada

        Returns:
            Entidade externa atualizada
        """
        nova_entidade_externa_dict = entidade_externa_input.convert_to_dict()
        # Insere no banco de dados e retorna a entidade externa
        return await self.entidade_externa_repo.update_entidade_externa_by_guid(guid, nova_entidade_externa_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar uma entidade externa pelo guid
        Args:
            guid: guid da entidade externa

        Returns:
            Nada
        """
        return await self.entidade_externa_repo.delete_entidade_externa_by_filtros(filtros=[EntidadeExternaModel.guid == guid])

