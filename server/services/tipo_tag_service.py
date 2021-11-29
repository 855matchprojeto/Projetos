from typing import Optional
from server.configuration.environment import Environment
from server.repository.tipo_tag_repository import TipoTagRepository
from server.models.tipo_tag_model import TipoDeTagModel
from sqlalchemy import or_, and_


class TipoTagService():

    def __init__(self, tipo_tag_repo: Optional[TipoTagRepository] = None, environment: Optional[Environment] = None):
        self.tipo_tag_repo = tipo_tag_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        """
        Método que faz a lógica de pegar os tipos de tags
        Args:
            id: id do tipo de tag
            guid: guid do tipo de tag

        Returns:
            Lista com os tipos de tags
        """
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    TipoDeTagModel.id == id,
                    TipoDeTagModel.guid == guid
                )]
        return await self.tipo_tag_repo.find_tipos_tag_by_filtros(filtros=filtros)

    async def create(self, tipo_tag_input):
        """
        Método que faz a lógica de criar um tipo de tag
        Args:
            tipo_tag_input: tipo de tag a ser criado

        Returns:
            Projeto criado
        """
        nova_tipo_tag_dict = tipo_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tipo_tag

        teste = await self.tipo_tag_repo.insere_tipo_tag(nova_tipo_tag_dict)
        return teste

    async def update(self, tipo_tag_input):
        """
        Método que faz a lógica de atualizar um tipo de tag
        Args:
            tipo_tag_input: tipo de tag a ser atualizado

        Returns:
            Tipo de tag atualizado
        """
        nova_tipo_tag_dict = tipo_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tipo_tag
        return await self.tipo_tag_repo.atualiza_tipo_tag(nova_tipo_tag_dict)

    async def update_by_guid(self, guid, tipo_tag_input):
        """
        Método que faz a lógica de atualizar um tipo de tag pelo guid
        Args:
            guid: guid do projeto
            tipo_tag_input: tipo de tag a ser atualizado

        Returns:
            Tipo de tag atualizado
        """
        nova_tipo_tag_dict = tipo_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tipo_tag
        return await self.tipo_tag_repo.update_tipo_tag_by_guid(guid, nova_tipo_tag_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar um tipo de tag pelo guid
        Args:
            guid: guid do tipo de tag

        Returns:
            Nada
        """
        return await self.tipo_tag_repo.delete_tipo_tag_by_filtros(filtros=[TipoDeTagModel.guid == guid])
