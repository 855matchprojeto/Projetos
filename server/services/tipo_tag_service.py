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
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    TipoDeTagModel.id == id,
                    TipoDeTagModel.guid == guid
                )]
        return await self.tipo_tag_repo.find_tipo_tags_by_filtros(filtros=filtros)

    async def create(self, tipo_tag_input):
        nova_tipo_tag_dict = tipo_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tipo_tag

        teste = await self.tipo_tag_repo.insere_tipo_tag(nova_tipo_tag_dict)
        return teste

    async def update(self, tipo_tag_input):
        nova_tipo_tag_dict = tipo_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tipo_tag
        return await self.tipo_tag_repo.atualiza_tipo_tag(nova_tipo_tag_dict)

    async def update_by_guid(self, guid, tipo_tag_input):
        nova_tipo_tag_dict = tipo_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a tipo_tag
        return await self.tipo_tag_repo.update_tipo_tag_by_guid(guid, nova_tipo_tag_dict)

    async def delete(self, guid):
        return await self.tipo_tag_repo.delete_tags_by_filtros(filtros=[TipoDeTagModel.guid == guid])
