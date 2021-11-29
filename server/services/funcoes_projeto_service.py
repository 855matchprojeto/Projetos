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
        """
        Método que faz a lógica de pegar as funções do projeto
        Args:
            id: id da função
            guid: guid da função

        Returns:
            Lista com as funções
        """
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
        """
        Método que faz a lógica de criar uma função
        Args:
            funcao_input: função a ser criada

        Returns:
            Função criada
        """
        nova_funcao_dict = funcao_input.convert_to_dict()
        # Insere no banco de dados e retorna a funcao

        teste = await self.func_repo.insere_funcao(nova_funcao_dict)
        return teste

    async def update(self, funcao_input):
        """
        Método que faz a lógica de atualizar uma função
        Args:
            funcao_input: função a ser atualizada

        Returns:
            Função atualizada
        """
        novo_funcao_dict = funcao_input.convert_to_dict()
        # Insere no banco de dados e retorna a funcao
        return await self.func_repo.atualiza_funcao(novo_funcao_dict)

    async def update_by_guid(self, guid, funcao_input):
        """
        Método que faz a lógica de atualizar uma função pelo guid
        Args:
            guid: guid da função
            funcao_input: função a ser atualizada

        Returns:
            Função atualizada
        """
        nova_funcao_dict = funcao_input.convert_to_dict()
        # Insere no banco de dados e retorna a funcao
        return await self.func_repo.update_funcao_by_guid(guid, nova_funcao_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar uma função pelo guid
        Args:
            guid: guid da função

        Returns:
            Nada
        """
        return await self.func_repo.delete_funcaos_by_filtros(filtros=[FuncaoProjetoModel.guid == guid])
