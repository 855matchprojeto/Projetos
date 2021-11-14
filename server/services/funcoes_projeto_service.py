from typing import List, Optional
from server.configuration.environment import Environment
from server.repository.funcoes_projeto_repository import FuncoesProjetoRepository
from server.models.funcao_projeto_model import FuncaoProjetoModel
from sqlalchemy import or_, and_


class FuncoesProjetoService():

    def __init__(self, func_repo: Optional[FuncoesProjetoRepository] = None, environment: Optional[Environment] = None):
        self.func_repo = func_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    FuncaoProjetoModel.id == id,
                    FuncaoProjetoModel.guid == guid
                )]
        return await self.func_repo.find_funcoes_by_filtros(filtros=filtros)

    async def create(self, funcao_input):
        nova_funcao_dict = funcao_input.convert_to_dict()
        # Insere no banco de dados e retorna a funcao

        teste = await self.func_repo.insere_funcao(nova_funcao_dict)
        return teste

    async def update(self, funcao_input):
        novo_funcao_dict = funcao_input.convert_to_dict()
        # Insere no banco de dados e retorna a funcao
        return await self.func_repo.atualiza_funcao(novo_funcao_dict)

    async def update_by_guid(self, guid, funcao_input):
        nova_funcao_dict = funcao_input.convert_to_dict()
        # Insere no banco de dados e retorna a funcao
        return await self.func_repo.update_funcao_by_guid(guid, nova_funcao_dict)

    async def delete(self, guid):
        return await self.func_repo.delete_funcaos_by_filtros(filtros=[FuncaoProjetoModel.guid == guid])
