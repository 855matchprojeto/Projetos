from server.configuration.db import AsyncSession
from server.configuration.exceptions import ProjectNotFoundException
from server.models.entidade_externa_model import EntidadeExternaModel
from server.models.funcao_projeto_model import FuncaoProjetoModel
from server.models.projetos_model import ProjetosModel
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.relacao_projeto_entidade import RelacaoProjetoEntidadeModel
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel
from server.models.tag_model import TagModel
from server.models.interesse_usuario_projeto_model import InteresseUsuarioProjeto
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel


class ProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_projeto(self, projeto_dict: dict) -> ProjetosModel:
        """
        Método que faz a query para inserir um projeto no banco de dados de projetos
        Args:
            projeto_dict: dicionário contendo os atributos do projeto

        Returns:
            Projeto criado
        """
        stmt = (
            insert(ProjetosModel).
                returning(literal_column('*')).
                values(**projeto_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return ProjetosModel(**row_to_dict)

    async def atualiza_projeto(self, projeto_dict: dict) -> ProjetosModel:
        """
        Método que faz a query para atualizar um projeto no banco de dados
        Args:
            projeto_dict: dicionário contendo os atributos do projeto

        Returns:
            Projeto atualizado
        """
        projeto_entity = ProjetosModel(**projeto_dict)
        self.db_session.add(projeto_entity)
        await self.db_session.flush()
        return projeto_entity

    async def update_projeto_by_guid(self, guid, projeto_update_dict: dict) -> ProjetosModel:
        """
        Método que faz a query para atualizar um projeto pelo guid no banco de dados
        Args:
            guid: guid do projeto
            projeto_update_dict: dicionário contendo os atributos do projeto

        Returns:
            Projeto atualizado
        """
        stmt = (
            update(ProjetosModel).
            returning(literal_column('*')).
            where(ProjetosModel.guid == guid).
            values(**projeto_update_dict)
        )
        query = await self.db_session.execute(stmt)
        if query.rowcount == 0:
            raise ProjectNotFoundException()
        row_to_dict = dict(query.fetchone())
        return ProjetosModel(**row_to_dict)

    async def find_projetos_by_filtros(self, filtros: List) -> List[ProjetosModel]:
        """
        Método que faz a query para pegar projetos por filtros no banco de dados
        Args:
            filtros: lista de ids de projetos

        Returns:
            Lista com projetos
        """
        stmt = (
            select(ProjetosModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_projetos_by_filtros(self, filtros: List):
        """
        Método que faz a query para deletar projetos por filtros no banco de dados
        Args:
            filtros: lista de ids de projetos

        Returns:
            Nada
        """
        stmt = (
            delete(ProjetosModel).
                where(*filtros)
        )
        await self.db_session.execute(stmt)

    async def find_projetos_by_ids(self) -> List[ProjetosModel]: #  project_ids: List[int]
        """
        Método que faz a query para pegar projetos por ids no banco de dados
        Esse método traz todas as informações associadas com o projeto
        Args:
            filtros: lista de ids de histórico de projetos

        Returns:
            Lista com projetos
        """
        stmt = (
            select(ProjetosModel)
            .distinct()
            .outerjoin(
                RelacaoProjetoEntidadeModel,
                RelacaoProjetoEntidadeModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                EntidadeExternaModel,
                RelacaoProjetoEntidadeModel.id_entidade == EntidadeExternaModel.id
            )
            .outerjoin(
                RelacaoProjetoTagModel,
                RelacaoProjetoTagModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                TagModel,
                RelacaoProjetoTagModel.id_tags == TagModel.id
            )
            .outerjoin(
                RelacaoProjetoUsuarioModel,
                RelacaoProjetoUsuarioModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                FuncaoProjetoModel,
                RelacaoProjetoUsuarioModel.id_funcao == FuncaoProjetoModel.id
            )
            .options(
                (
                    selectinload(ProjetosModel.rel_projeto_entidade).
                    selectinload(RelacaoProjetoEntidadeModel.entidade_externa)
            ),
                (
                    selectinload(ProjetosModel.rel_projeto_tag).
                    selectinload(RelacaoProjetoTagModel.tag)
            ),
                (
                    selectinload(ProjetosModel.rel_projeto_usuario).
                    selectinload(RelacaoProjetoUsuarioModel.funcao)
            )
            )

        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def insere_interesse_usuario_projeto(self, guid_usuario: str, id_projeto: int) -> InteresseUsuarioProjeto:
        stmt = (
            insert(InteresseUsuarioProjeto).
            returning(literal_column('*')).
            values(
                id_projeto=id_projeto,
                guid_usuario=guid_usuario
            )
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return InteresseUsuarioProjeto(**row_to_dict)

    async def delete_interesse_usuario_projeto_by_filtros(self, filtros) -> None:
        stmt = (
            delete(InteresseUsuarioProjeto).
            where(*filtros)
        )
        await self.db_session.execute(stmt)

    async def get_projetos_interesse_usuario(self, guid_usuario: str):
        """
            Captura os projetos que o usuário marcou como interesse
        """
        stmt = (
            select(ProjetosModel).
            join(
                InteresseUsuarioProjeto,
                InteresseUsuarioProjeto.id_projeto == ProjetosModel.id
            ).
            where(InteresseUsuarioProjeto.guid_usuario == guid_usuario)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def get_projetos_usuario(self, guid_usuario: str):
        """
            Captura os projetos em que o usuário está presente
            com algum vínculo de função
        """
        stmt = (
            select(ProjetosModel).
            join(
                RelacaoProjetoUsuarioModel,
                RelacaoProjetoUsuarioModel.id_projetos == ProjetosModel.id
            ).
            where(RelacaoProjetoUsuarioModel.guid_user == guid_usuario)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def insere_relacao_usuario_funcao_projeto(
        self, id_funcao: int, guid_usuario: str, id_projeto: int
    ):
        """
            Vincula uma função de projeto para um
            usuário
        """
        stmt = (
            insert(RelacaoProjetoUsuarioModel).
            returning(literal_column('*')).
            values(
                id_projetos=id_projeto,
                id_funcao=id_funcao,
                guid_user=guid_usuario
            )
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return RelacaoProjetoUsuarioModel(**row_to_dict)

    async def get_owners_projeto(self, id_projeto: int) -> List[str]:
        """
            Captura os owners de um projeto
            Retorna o guids dos owners de um projeto
        """
        stmt = (
            select(RelacaoProjetoUsuarioModel).
            join(
                FuncaoProjetoModel,
                FuncaoProjetoModel.id == RelacaoProjetoUsuarioModel.id_funcao
            ).
            where(
                RelacaoProjetoUsuarioModel.id_projetos == id_projeto,
                FuncaoProjetoModel.nome == 'OWNER'
            )
        )

        query = await self.db_session.execute(stmt)
        relacoes: List[RelacaoProjetoUsuarioModel] = query.scalars().all()

        return [
            str(relacao.guid_user) for relacao in relacoes
        ]

