from server.configuration.db import AsyncSession
from server.configuration.exceptions import ProjectNotFoundException
from server.models.entidade_externa_model import EntidadeExternaModel
from server.models.funcao_projeto_model import FuncaoProjetoModel
from server.models.projetos_model import ProjetosModel
from sqlalchemy.orm import selectinload, contains_eager
from sqlalchemy import select, insert, literal_column, delete, update
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.relacao_projeto_entidade import RelacaoProjetoEntidadeModel
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel
from server.models.tag_model import TagModel
from server.models.interesse_usuario_projeto_model import InteresseUsuarioProjeto
from server.models.relacao_projeto_usuario_model import RelacaoProjetoUsuarioModel
from server.models.curso_model import CursoModel
from server.models.interesse_model import InteresseModel
from server.models.relacao_projeto_curso import RelacaoProjetoCursoModel
from server.models.relacao_projeto_interesse import RelacaoProjetoInteresseModel
from server.schemas.cursor_schema import Cursor
from jose import jwt


class ProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    def encode_cursor(self, cursor: dict):
        return jwt.encode(
            cursor,
            self.environment.CURSOR_TOKEN_SECRET_KEY,
            algorithm=self.environment.CURSOR_TOKEN_ALGORITHM
        )

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

    async def find_projetos_by_ids(self, filtros) -> List[ProjetosModel]: #  project_ids: List[int]
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
            .outerjoin(
                RelacaoProjetoCursoModel,
                RelacaoProjetoCursoModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                CursoModel,
                RelacaoProjetoCursoModel.id_cursos == CursoModel.id
            )
            .outerjoin(
                RelacaoProjetoInteresseModel,
                RelacaoProjetoInteresseModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                InteresseModel,
                RelacaoProjetoInteresseModel.id_interesses == InteresseModel.id
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
            ),
                (
                    selectinload(ProjetosModel.rel_projeto_curso).
                        selectinload(RelacaoProjetoCursoModel.curso)
            ),
                (
                    selectinload(ProjetosModel.relacao_projeto_interesse).
                        selectinload(RelacaoProjetoInteresseModel.interesse)
            )
            ).where(*filtros)

        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()


    async def find_projetos_paginated(self, filters, limit, cursor: Cursor) -> List[ProjetosModel]: #  project_ids: List[int]
        """
        Método que faz a query para pegar projetos por ids no banco de dados paginado
        Esse método traz todas as informações associadas com o projeto
        Args:
            filtros: lista de ids de histórico de projetos

        Returns:
            Lista com projetos
        """

        # Offset a partir do cursor, geralmente é pelo ID
        # Limit + 1 para capturar o ultimo perfil. Esse último perfil será usado no cursor
        if cursor:
            filters.append(ProjetoRepository.build_cursor_filter(cursor))

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
            .outerjoin(
                RelacaoProjetoCursoModel,
                RelacaoProjetoCursoModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                CursoModel,
                RelacaoProjetoCursoModel.id_cursos == CursoModel.id
            )
            .outerjoin(
                RelacaoProjetoInteresseModel,
                RelacaoProjetoInteresseModel.id_projetos == ProjetosModel.id
            )
            .outerjoin(
                InteresseModel,
                RelacaoProjetoInteresseModel.id_interesses == InteresseModel.id
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
            ),
                (
                    selectinload(ProjetosModel.rel_projeto_curso).
                        selectinload(RelacaoProjetoCursoModel.curso)
            ),
                (
                    selectinload(ProjetosModel.relacao_projeto_interesse).
                        selectinload(RelacaoProjetoInteresseModel.interesse)
            )
            ).where(*filters).limit(limit+1).order_by(
            ProjetosModel.titulo.asc()
        )

        )
        query = await self.db_session.execute(stmt)
        projetos = query.scalars().all()

        # Capturando o ultimo perfil e setando o next_cursor
        next_cursor = None
        if len(projetos) == (limit + 1):
            last_project = projetos[limit]
            next_cursor = {
                'sort_field_key': cursor.sort_field_key if cursor else 'titulo',
                'sort_field_type': cursor.sort_field_type if cursor else 'str',
                'operator': 'ge',
                'value': last_project.titulo
            }

        return {
            "items": projetos[:limit],
            "next_cursor": self.encode_cursor(next_cursor) if next_cursor else None,
            "count": len(projetos[:limit])
        }

    @staticmethod
    def update_body_if_match(obj_in_db: InteresseUsuarioProjeto, body: dict):
        fl_usuario_interesse = (
           body['fl_usuario_interesse']
           if 'fl_usuario_interesse' in body
           else obj_in_db.fl_usuario_interesse if obj_in_db else False
        )

        fl_projeto_interesse = (
            body['fl_projeto_interesse']
            if 'fl_projeto_interesse' in body
            else obj_in_db.fl_projeto_interesse if obj_in_db else False
        )

        fl_match = fl_usuario_interesse and fl_projeto_interesse

        body['fl_match'] = fl_match

    async def upsert_interesse_usuario_projeto(
        self, guid_usuario: str, id_projeto: int, body: dict,
        obj_in_db: Optional[InteresseUsuarioProjeto] = None
    ) -> InteresseUsuarioProjeto:
        self.update_body_if_match(obj_in_db, body)

        if obj_in_db:
            return await self.update_interesse_usuario_projeto(guid_usuario, id_projeto, body)
        return await self.insert_interesse_usuario_projeto(guid_usuario, id_projeto, body)

    async def find_interesse_usuario_projeto(
        self, guid_usuario: str, id_projeto: int
    ) -> InteresseUsuarioProjeto:
        stmt = (
            select(InteresseUsuarioProjeto).
            where(
                InteresseUsuarioProjeto.guid_usuario == guid_usuario,
                InteresseUsuarioProjeto.id_projeto == id_projeto
            )
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().first()

    async def update_interesse_usuario_projeto(
        self, guid_usuario: str, id_projeto: int, body: dict
    ) -> InteresseUsuarioProjeto:
        stmt = (
            update(InteresseUsuarioProjeto).
            where(
                InteresseUsuarioProjeto.id_projeto == id_projeto,
                InteresseUsuarioProjeto.guid_usuario == guid_usuario,
            ).
            returning(literal_column('*')).
            values(**body)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return InteresseUsuarioProjeto(**row_to_dict)

    async def insert_interesse_usuario_projeto(
        self, guid_usuario: str, id_projeto: int, body: dict
    ) -> InteresseUsuarioProjeto:
        stmt = (
            insert(InteresseUsuarioProjeto).
            returning(literal_column('*')).
            values(
                id_projeto=id_projeto,
                guid_usuario=guid_usuario,
                **body
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

    async def get_usuarios_interessados_projeto(self, guid_projeto: str, filters=None):
        """
            Captura os usuários interessados pelo projeto a partir da tabela
            tb_interesse_usuario_projeto
        """

        if not filters:
            filters = []
        filters.append(ProjetosModel.guid == guid_projeto)

        stmt = (
            select(InteresseUsuarioProjeto).
            join(
                ProjetosModel,
                InteresseUsuarioProjeto.id_projeto == ProjetosModel.id
            ).
            where(*filters)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def get_projetos_interesse_usuario(self, guid_usuario: str, filters=None):
        """
            Captura os projetos que o usuário está marcado como interesse
            em alguma das partes
        """

        if not filters:
            filters = []
        filters.append(InteresseUsuarioProjeto.guid_usuario == guid_usuario)

        stmt = (
            select(ProjetosModel).
            join(
                InteresseUsuarioProjeto,
                InteresseUsuarioProjeto.id_projeto == ProjetosModel.id
            ).
            where(*filters).
            options(
                contains_eager(
                    ProjetosModel.rel_projeto_interesse,
                )
            ).
            execution_options(populate_existing=True)
        )

        query = await self.db_session.execute(stmt)

        row_list = query.unique().all()
        projetos_dict = [
            dict(row)['ProjetosModel'].__dict__ for row in row_list
        ]

        for projeto_dict in projetos_dict:
            interesse_usuario_projeto = projeto_dict.pop('rel_projeto_interesse')

            projeto_dict['interesse_usuario_projeto'] = (
                interesse_usuario_projeto[0] if interesse_usuario_projeto else None
            )

        return projetos_dict

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

