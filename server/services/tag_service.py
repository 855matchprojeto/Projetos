from typing import Optional
from server.configuration.environment import Environment
from server.repository.tag_repository import TagRepository
from server.models.tag_model import TagModel
from sqlalchemy import or_, and_


class TagService():

    def __init__(self, tag_repo: Optional[TagRepository] = None, environment: Optional[Environment] = None):
        self.tag_repo = tag_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        """
        Método que faz a lógica de pegar as tags
        Args:
            id: id da tag
            guid: guid da tag

        Returns:
            Lista com as tags
        """
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    TagModel.id == id,
                    TagModel.guid == guid
                )]
        return await self.tag_repo.find_tags_by_filtros(filtros=filtros)

    async def create(self, tag_input):
        """
        Método que faz a lógica de criar uma tag
        Args:
            tag_input: tag a ser criada

        Returns:
            Tag criada
        """
        nova_tag_dict = tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tag

        teste = await self.tag_repo.insere_tag(nova_tag_dict)
        return teste

    async def update(self, tag_input):
        """
        Método que faz a lógica de atualizar uma tag
        Args:
            tag_input: tag a ser atualizada

        Returns:
            Tag atualizada
        """
        nova_tag_dict = tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tag
        return await self.tag_repo.atualiza_tag(nova_tag_dict)

    async def update_by_guid(self, guid, tag_input):
        """
        Método que faz a lógica de atualizar uma tag pelo guid
        Args:
            guid: guid da tag
            tag_input: tag a ser atualizada

        Returns:
            Tag atualizada
        """
        nova_tag_dict = tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tag
        return await self.tag_repo.update_tag_by_guid(guid, nova_tag_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar uma tag pelo guid
        Args:
            guid: guid da tag

        Returns:
            Nada
        """
        return await self.tag_repo.delete_tags_by_filtros(filtros=[TagModel.guid == guid])
