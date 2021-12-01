from typing import List, Optional
from server.configuration.environment import Environment
from server.repository.projetos_repository import ProjetoRepository
from server.models.projetos_model import ProjetosModel
from sqlalchemy import or_, and_
from server.configuration import exceptions
from server.models.interesse_usuario_projeto_model import InteresseUsuarioProjeto
from server.repository.funcoes_projeto_repository import FuncoesProjetoRepository
from server.models.funcao_projeto_model import FuncaoProjetoModel


class ProjetosService:

    def __init__(
        self,
        proj_repo: Optional[ProjetoRepository] = None,
        environment: Optional[Environment] = None,
        funcao_proj_repo: Optional[FuncoesProjetoRepository] = None
    ):
        self.proj_repo = proj_repo
        self.funcao_proj_repo = funcao_proj_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        """
        Método que faz a lógica de pegar os projetos
        Args:
            id: id do projeto
            guid: guid do projeto

        Returns:
            Lista com os projetos
        """
        if id == None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    ProjetosModel.id == id,
                    ProjetosModel.guid == guid
                )]

        projects = await self.proj_repo.find_projetos_by_ids()  # filtros=filtros
        for project in projects:
            entidades = [rel_projeto_entidade.entidade_externa for rel_projeto_entidade in project.rel_projeto_entidade]
            tags = [rel_projeto_tag.tag for rel_projeto_tag in project.rel_projeto_tag]
            project.entidades = entidades
            project.tags = tags

        return projects

    async def create(self, projeto_input):
        """
        Método que faz a lógica de criar um projeto
        Args:
            projeto_input: projeto a ser criado

        Returns:
            Projeto criado
        """
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto
        projeto = await self.proj_repo.insere_projeto(novo_projeto_dict)
        # Vinculando o usuário com uma função de owner
        await self.link_user_as_owner(guid_usuario, projeto)
        return projeto

    async def link_user_as_owner(self, guid_usuario: str, projeto: ProjetosModel):
        # Captura a função de OWNER no banco de dados
        owner_filter = [FuncaoProjetoModel.nome == "OWNER"]
        funcao_owner = await self.funcao_proj_repo.find_funcoes_by_filtros(owner_filter)
        if len(funcao_owner) == 0:
            raise exceptions.FuncaoProjectNotFoundException(
                detail="Não foi encontrada uma função de OWNER no sistema!"
            )
        funcao_owner = funcao_owner[0]
        # Vinculando o usuário com a função no projeto
        await self.proj_repo.insere_relacao_usuario_funcao_projeto(
            funcao_owner.id, guid_usuario, projeto.id
        )

    async def update(self, projeto_input):
        """
        Método que faz a lógica de atualizar um projeto
        Args:
            projeto_input: projeto a ser atualizado

        Returns:
            Projeto atualizado
        """
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto
        return await self.proj_repo.atualiza_projeto(novo_projeto_dict)

    async def update_by_guid(self, guid, projeto_input):
        """
        Método que faz a lógica de atualizar um projeto pelo guid
        Args:
            guid: guid do projeto
            projeto_input: projeto a ser atualizado

        Returns:
            Projeto atualizado
        """
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto
        return await self.proj_repo.update_projeto_by_guid(guid, novo_projeto_dict)

    async def delete(self, guid):
        """
        Método que faz a lógica de deletar um projeto pelo guid
        Args:
            guid: guid do projeto

        Returns:
            Nada
        """
        await self.proj_repo.delete_projetos_by_filtros(filtros=[ProjetosModel.guid == guid])

    async def insert_interesse_usuario_projeto(self, guid_usuario: str, guid_projeto: str):
        # Capturando ID do projeto e verifcando sua existência
        projetos_db = await self.proj_repo.find_projetos_by_filtros(
            filtros=[ProjetosModel.guid == guid_projeto]
        )
        if len(projetos_db) == 0:
            raise exceptions.ProjectNotFoundException(
                detail=f"Não foi encontrado um projeto com GUID = {guid_projeto}"
            )
        # Vinculando as duas entidades, criando um interesse do usuário pelo projeto
        projeto = projetos_db[0]
        return await self.proj_repo.insere_interesse_usuario_projeto(
            guid_usuario,
            projeto.id
        )

    async def delete_interesse_usuario_projeto(self, guid_usuario: str, guid_projeto: str):
        # Capturando ID do projeto e verifcando sua existência
        projetos_db = await self.proj_repo.find_projetos_by_filtros(
            filtros=[ProjetosModel.guid == guid_projeto]
        )
        if len(projetos_db) == 0:
            raise exceptions.ProjectNotFoundException(
                detail=f"Não foi encontrado um projeto com GUID = {guid_projeto}"
            )
        projeto = projetos_db[0]
        # Deleta entidade de "InteresseUsuarioProjeto" a partir do ID do projeto e do guid do usuario
        await self.proj_repo.delete_interesse_usuario_projeto_by_filtros(
            [
                InteresseUsuarioProjeto.guid_usuario == guid_usuario,
                InteresseUsuarioProjeto.id_projeto == projeto.id
            ]
        )

    async def get_projetos_interesse_usuario(self, guid_usuario: str):
        """
            Captura os projetos que o usuário
            marcou como seu interesse
        """
        return await self.proj_repo.get_projetos_interesse_usuario(guid_usuario)

    async def get_projetos_usuario(self, guid_usuario: str):
        """
            Captura os projetos que o usuário
            pertence com algum vínculo de função no projeto
        """
        return await self.proj_repo.get_projetos_usuario(guid_usuario)

