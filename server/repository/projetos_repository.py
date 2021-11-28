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


class ProjetoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_projeto(self, projeto_dict: dict) -> ProjetosModel:
        stmt = (
            insert(ProjetosModel).
                returning(literal_column('*')).
                values(**projeto_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return ProjetosModel(**row_to_dict)

    async def atualiza_projeto(self, projeto_dict: dict) -> ProjetosModel:
        projeto_entity = ProjetosModel(**projeto_dict)
        self.db_session.add(projeto_entity)
        await self.db_session.flush()
        return projeto_entity

    async def update_projeto_by_guid(self, guid, projeto_update_dict: dict) -> ProjetosModel:
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
        stmt = (
            select(ProjetosModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def delete_projetos_by_filtros(self, filtros: List):
        stmt = (
            delete(ProjetosModel).
                where(*filtros)
        )
        query = await self.db_session.execute(stmt)
        return query.scalars().all()

    async def find_projetos_by_ids(self) -> List[ProjetosModel]: #  project_ids: List[int]
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

