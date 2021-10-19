from typing import List, Optional
from server.configuration.environment import Environment
from server.repository.projetos_repository import ProjetoRepository
from server.models.projetos_model import ProjetosModel
from sqlalchemy import or_, and_


class ProjetosService():
    """Classe definida para representar a lógica especifica de um Projeto
    """

    def __init__(self, proj_repo: Optional[ProjetoRepository] = None, environment: Optional[Environment] = None):
        self.proj_repo = proj_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        filtros = [
            or_(
                ProjetosModel.id == id,
                ProjetosModel.guid == guid
            )]
        return await self.proj_repo.find_projetos_by_filtros(filtros=filtros)

    async def create(self, projeto_input):
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto

        teste = await self.proj_repo.insere_projeto(novo_projeto_dict)
        return teste

    async def update(self, projeto_input):
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto
        return await self.proj_repo.atualiza_projeto(novo_projeto_dict)

    async def update_by_guid(self, guid, projeto_input):
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto
        return await self.proj_repo.update_projeto_by_guid(guid, novo_projeto_dict)

    async def delete(self, guid):
        return await self.proj_repo.delete_projetos_by_filtros(filtros=[ProjetosModel.guid == guid])

