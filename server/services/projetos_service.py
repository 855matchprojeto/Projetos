from fastapi import Request
from typing import List, Optional
from server.configuration.environment import Environment
from server.models.arquivo_model import Arquivo
from server.repository.projetos_repository import ProjetoRepository
from jose import jwt
from server.models.projetos_model import ProjetosModel
from sqlalchemy import or_, and_
from server.configuration import exceptions
from server.models.interesse_usuario_projeto_model import InteresseUsuarioProjeto
from server.repository.funcoes_projeto_repository import FuncoesProjetoRepository
from server.models.funcao_projeto_model import FuncaoProjetoModel
from typing import Any
import json
from server.schemas.usuario_schema import CurrentUserToken
from server.services.arquivo_service import ArquivoService
from server.schemas.projetos_schema import ProjetosInput
from server.schemas.interesse_usuario_projeto_schema import InteresseUsuarioProjetoInput
from server.schemas.cursor_schema import Cursor
from server.models.curso_model import CursoModel
from server.models.interesse_model import InteresseModel


class ProjetosService:

    def decode_cursor_info(self, encoded_cursor: str):
        decoded_cursor_dict = jwt.decode(
            encoded_cursor,
            self.environment.CURSOR_TOKEN_SECRET_KEY,  # verificar
            algorithms=[self.environment.CURSOR_TOKEN_ALGORITHM]
        )
        return Cursor(**decoded_cursor_dict)

    @staticmethod
    def build_projeto_payload(projeto: ProjetosModel):
        return {
            'id': projeto.id,
            'guid': str(projeto.guid),
            'titulo': projeto.titulo,
            'descricao': projeto.descricao,
            'url_imagem': (
                projeto.imagem_projeto.url
                if projeto.imagem_projeto
                else None
            )
        }

    @staticmethod
    def build_interesse_usuario_projeto_msg_payload(
            guid_usuario: str, owners: List[str], projeto: ProjetosModel
    ):
        payload_dict = dict(
            type='INTERESSE_USUARIO_PROJETO',
            user={
                'guid_usuario': guid_usuario,
            },
            project=ProjetosService.build_projeto_payload(projeto),
            owners=owners
        )
        return json.dumps(payload_dict)

    @staticmethod
    def build_interesse_projeto_usuario_msg_payload(
            guid_usuario: str, projeto: ProjetosModel
    ):
        payload_dict = dict(
            type='INTERESSE_PROJETO_USUARIO',
            user={
                'guid_usuario': guid_usuario,
            },
            project=ProjetosService.build_projeto_payload(projeto),
        )
        return json.dumps(payload_dict)

    @staticmethod
    def build_match_msg_payload(
            guid_usuario: str, owners: List[str], projeto: ProjetosModel
    ):
        payload_dict = dict(
            type='MATCH',
            user={
                'guid_usuario': guid_usuario,
            },
            project=ProjetosService.build_projeto_payload(projeto),
            owners=owners
        )
        return json.dumps(payload_dict)

    @staticmethod
    def get_previous_url(request: Request):
        return str(request.url)

    @staticmethod
    def get_next_url(request: Request, path: str, next_encoded_cursor: str):
        if not next_encoded_cursor:
            return None

        query_params_dict = dict(request.query_params)
        query_string_builder = '?'

        for query_param_key in [key for key in query_params_dict.keys() if key != 'cursor']:
            query_param_value = query_params_dict[query_param_key]
            query_string_builder += f'{query_param_key}={query_param_value}&'

        query_string_builder += f'cursor={next_encoded_cursor}'

        return f"{request.base_url}{path}{query_string_builder}"

    @staticmethod
    def handle_projetos_pagination(
            paginated_projeto_dict: dict, previous_encoded_cursor: str, request: Request
    ):
        next_encoded_cursor = paginated_projeto_dict['next_cursor']
        paginated_projeto_dict['previous_cursor'] = previous_encoded_cursor
        paginated_projeto_dict['previous_url'] = ProjetosService.get_previous_url(request)
        paginated_projeto_dict['next_url'] = ProjetosService.get_next_url(request, request.url.path,
                                                                          next_encoded_cursor)
        return paginated_projeto_dict

    def __init__(
            self,
            proj_repo: Optional[ProjetoRepository] = None,
            environment: Optional[Environment] = None,
            arquivo_service: Optional[ArquivoService] = None,
            funcao_proj_repo: Optional[FuncoesProjetoRepository] = None,
            publisher_service: Optional[Any] = None
    ):
        self.proj_repo = proj_repo
        self.funcao_proj_repo = funcao_proj_repo
        self.environment = environment
        self.publisher_service = publisher_service
        self.arquivo_service = arquivo_service

    async def handle_input_imagem_perfil(
            self, current_user: CurrentUserToken, projeto_input: ProjetosInput
    ) -> Optional[Arquivo]:
        """
            Cria o arquivo da imagem do projeto do usuario e vincula
            o id do arquivo criado no input
        """

        imagem_projeto_input = projeto_input.get('imagem_projeto')
        if imagem_projeto_input:
            imagem_projeto = await self.arquivo_service.upload_arquivo(imagem_projeto_input, current_user)

            projeto_input["id_imagem_projeto"] = imagem_projeto.id
            del projeto_input["imagem_projeto"]

            return imagem_projeto

        return None

    async def get(self, id=None, guid=None, titulo_ilike=None, curso_nome_referencia=None,
                  projects_query_params=None,
                  interesse_nome_referencia=None):
        """
        M??todo que faz a l??gica de pegar os projetos
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

        if titulo_ilike:
            filtros.append(ProjetosModel.titulo.ilike(f'%{titulo_ilike}%'))

        if curso_nome_referencia:
            filtros.append(CursoModel.nome_referencia.ilike(f'%{curso_nome_referencia}%'))

        if interesse_nome_referencia:
            filtros.append(InteresseModel.nome_referencia.ilike(f'%{interesse_nome_referencia}%'))

        if titulo_ilike:
            filtros.append(ProjetosModel.titulo.ilike(f'%{titulo_ilike}%'))

        if projects_query_params and projects_query_params['interests_in']:
            filtros.append(InteresseModel.id.in_(projects_query_params['interests_in']))

        if projects_query_params and projects_query_params['courses_in']:
            filtros.append(CursoModel.id.in_(projects_query_params['courses_in']))

        projects = await self.proj_repo.find_projetos_by_ids(filtros=filtros)
        for project in projects:
            entidades = [rel_projeto_entidade.entidade_externa for rel_projeto_entidade in project.rel_projeto_entidade]
            tags = [rel_projeto_tag.tag for rel_projeto_tag in project.rel_projeto_tag]
            cursos = [rel_projeto_curso.curso for rel_projeto_curso in project.rel_projeto_curso]
            interesses = [relacao_projeto_interesse.interesse for relacao_projeto_interesse in
                          project.relacao_projeto_interesse]
            project.entidades = entidades
            project.tags = tags
            project.cursos = cursos
            project.interesses = interesses

        return projects

    async def get_paginated(self, request: Request, limit: int, cursor: str, id=None, guid=None, titulo_ilike=None,
                            curso_nome_referencia=None,
                            interesse_nome_referencia=None, projects_query_params=None):
        """
        M??todo que faz a l??gica de pegar os projetos paginados
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

        if titulo_ilike:
            filtros.append(ProjetosModel.titulo.ilike(f'%{titulo_ilike}%'))

        if curso_nome_referencia:
            filtros.append(CursoModel.nome_referencia.ilike(f'%{curso_nome_referencia}%'))

        if interesse_nome_referencia:
            filtros.append(InteresseModel.nome_referencia.ilike(f'%{interesse_nome_referencia}%'))

        if projects_query_params and projects_query_params['interests_in']:
            filtros.append(InteresseModel.id.in_(projects_query_params['interests_in']))

        if projects_query_params and projects_query_params['courses_in']:
            filtros.append(CursoModel.id.in_(projects_query_params['courses_in']))

        decoded_cursor = self.decode_cursor_info(cursor) if cursor else None

        # projects = await self.proj_repo.find_projetos_by_ids(filtros=filtros)

        paginated_projects_dict = await self.proj_repo. \
            find_projetos_paginated(limit=limit, cursor=decoded_cursor, filters=filtros)

        paginated_projects_dict = ProjetosService.handle_projetos_pagination(
            paginated_projects_dict, cursor, request
        )

        for project in paginated_projects_dict['items']:
            entidades = [rel_projeto_entidade.entidade_externa for rel_projeto_entidade in project.rel_projeto_entidade]
            tags = [rel_projeto_tag.tag for rel_projeto_tag in project.rel_projeto_tag]
            cursos = [rel_projeto_curso.curso for rel_projeto_curso in project.rel_projeto_curso]
            interesses = [relacao_projeto_interesse.interesse for relacao_projeto_interesse in
                          project.relacao_projeto_interesse]
            project.entidades = entidades
            project.tags = tags
            project.cursos = cursos
            project.interesses = interesses

        return paginated_projects_dict

    async def create(self, projeto_input, current_user: CurrentUserToken):
        """
        M??todo que faz a l??gica de criar um projeto
        Args:
            current_user: usu??rio
            projeto_input: projeto a ser criado

        Returns:
            Projeto criado
        """
        if type(projeto_input) is not dict:
            projeto_input = projeto_input.convert_to_dict()

        await self.handle_input_imagem_perfil(current_user, projeto_input)
        # Insere no banco de dados e retorna o projeto
        projeto = await self.proj_repo.insere_projeto(projeto_input)
        # Vinculando o usu??rio com uma fun????o de owner
        await self.link_user_as_owner(current_user.guid, projeto)
        return projeto

    async def link_user_as_owner(self, guid_usuario: str, projeto: ProjetosModel):
        # Captura a fun????o de OWNER no banco de dados
        owner_filter = [FuncaoProjetoModel.nome == "OWNER"]
        funcao_owner = await self.funcao_proj_repo.find_funcoes_by_filtros(owner_filter)
        if len(funcao_owner) == 0:
            raise exceptions.FuncaoProjectNotFoundException(
                detail="N??o foi encontrada uma fun????o de OWNER no sistema!"
            )
        funcao_owner = funcao_owner[0]
        # Vinculando o usu??rio com a fun????o no projeto
        await self.proj_repo.insere_relacao_usuario_funcao_projeto(
            funcao_owner.id, guid_usuario, projeto.id
        )

    async def update(self, projeto_input):
        """
        M??todo que faz a l??gica de atualizar um projeto
        Args:
            projeto_input: projeto a ser atualizado

        Returns:
            Projeto atualizado
        """
        novo_projeto_dict = projeto_input.convert_to_dict()
        # Insere no banco de dados e retorna o projeto
        return await self.proj_repo.atualiza_projeto(novo_projeto_dict)

    async def update_by_guid(self, guid, projeto_input, current_user):
        """
        M??todo que faz a l??gica de atualizar um projeto pelo guid
        Args:
            guid: guid do projeto
            projeto_input: projeto a ser atualizado

        Returns:
            Projeto atualizado
        """
        novo_projeto_dict = projeto_input.convert_to_dict()
        await self.handle_input_imagem_perfil(current_user, novo_projeto_dict)
        # Insere no banco de dados e retorna o projeto
        return await self.proj_repo.update_projeto_by_guid(guid, novo_projeto_dict)

    async def delete(self, guid):
        """
        M??todo que faz a l??gica de deletar um projeto pelo guid
        Args:
            guid: guid do projeto

        Returns:
            Nada
        """
        await self.proj_repo.delete_projetos_by_filtros(filtros=[ProjetosModel.guid == guid])

    async def insert_interesse_usuario_projeto(self, current_user: CurrentUserToken, guid_projeto: str):
        # Capturando ID do projeto e verifcando sua exist??ncia
        projetos_db = await self.proj_repo.find_projetos_by_filtros(
            filtros=[ProjetosModel.guid == guid_projeto]
        )
        if len(projetos_db) == 0:
            raise exceptions.ProjectNotFoundException(
                detail=f"N??o foi encontrado um projeto com GUID = {guid_projeto}"
            )
        # Vinculando as duas entidades, criando um interesse do usu??rio pelo projeto
        projeto = projetos_db[0]
        interesse_usuario_projeto = await self.proj_repo.insere_interesse_usuario_projeto(
            current_user.guid,
            projeto.id
        )

        await self.publish_usuario_projeto_interesse_notification(current_user.guid, projeto)

        return interesse_usuario_projeto

    async def publish_match_notification(
            self, guid_usuario: str, projeto: ProjetosModel
    ):
        return self.publisher_service.publish(
            self.build_match_msg_payload(
                guid_usuario, await self.proj_repo.get_owners_projeto(projeto.id), projeto
            ),
            self.environment.INTERESSE_USUARIO_PROJETO_ARN
        )

    async def publish_projeto_usuario_interesse_notification(
            self, guid_usuario: str, projeto: ProjetosModel
    ):
        # Define um payload para a mensagem de cria????o
        # de interesse de um projeto para um usu??rio para o publicador de mensagem

        return self.publisher_service.publish(
            self.build_interesse_projeto_usuario_msg_payload(
                guid_usuario, projeto
            ),
            self.environment.INTERESSE_USUARIO_PROJETO_ARN
        )

    async def publish_usuario_projeto_interesse_notification(
            self, guid_usuario: str, projeto: ProjetosModel
    ):
        # Define um payload para a mensagem de cria????o
        # de interesse de um usu??rio para o projeto para o publicador de mensagem

        return self.publisher_service.publish(
            self.build_interesse_usuario_projeto_msg_payload(
                guid_usuario, await self.proj_repo.get_owners_projeto(projeto.id), projeto
            ),
            self.environment.INTERESSE_USUARIO_PROJETO_ARN
        )

    async def publish_notification_interesse(
            self, projeto: ProjetosModel, old_interesse_usuario_projeto: InteresseUsuarioProjeto,
            interesse_usuario_projeto: InteresseUsuarioProjeto, input_body_dict: dict
    ):
        fl_changed_usuario_interesse = (
                input_body_dict.get('fl_usuario_interesse') and
                (
                        not old_interesse_usuario_projeto or
                        input_body_dict.get(
                            'fl_usuario_interesse') != old_interesse_usuario_projeto.fl_usuario_interesse
                )
        )

        fl_changed_projeto_interesse = (
                input_body_dict.get('fl_projeto_interesse') and
                (
                        not old_interesse_usuario_projeto or
                        input_body_dict.get(
                            'fl_projeto_interesse') != old_interesse_usuario_projeto.fl_projeto_interesse
                )
        )

        if fl_changed_usuario_interesse or fl_changed_projeto_interesse:
            fl_match = interesse_usuario_projeto.fl_match

            if fl_match:
                return await self.publish_match_notification(
                    str(interesse_usuario_projeto.guid_usuario), projeto)

            return (
                await self.publish_usuario_projeto_interesse_notification(
                    str(interesse_usuario_projeto.guid_usuario), projeto)
                if fl_changed_usuario_interesse
                else await self.publish_projeto_usuario_interesse_notification(
                    str(interesse_usuario_projeto.guid_usuario), projeto)
            )

    async def upsert_interesse_usuario_projeto(
            self, guid_usuario: str, guid_projeto: str, input_body: InteresseUsuarioProjetoInput
    ):
        # Capturando ID do projeto e verificando sua exist??ncia
        projetos_db = await self.proj_repo.find_projetos_by_ids(
            filtros=[ProjetosModel.guid == guid_projeto]
        )
        if len(projetos_db) == 0:
            raise exceptions.ProjectNotFoundException(
                detail=f"N??o foi encontrado um projeto com GUID = {guid_projeto}"
            )
        projeto = projetos_db[0]

        # Criando ou atualizando o interesse do usu??rio pelo projeto (ou vice-versa)
        input_body_dict = input_body.dict(exclude_unset=True)

        old_interesse_usuario_projeto = await self.proj_repo.find_interesse_usuario_projeto(guid_usuario, projeto.id)

        interesse_usuario_projeto = \
            await self.proj_repo.upsert_interesse_usuario_projeto(
                guid_usuario, projeto.id, input_body.dict(exclude_unset=True), old_interesse_usuario_projeto
            )

        # Publica????o de notifica????es
        await self.publish_notification_interesse(
            projeto, old_interesse_usuario_projeto, interesse_usuario_projeto, input_body_dict)

        return interesse_usuario_projeto

    async def delete_interesse_usuario_projeto(self, guid_usuario: str, guid_projeto: str):
        # Capturando ID do projeto e verifcando sua exist??ncia
        projetos_db = await self.proj_repo.find_projetos_by_filtros(
            filtros=[ProjetosModel.guid == guid_projeto]
        )
        if len(projetos_db) == 0:
            raise exceptions.ProjectNotFoundException(
                detail=f"N??o foi encontrado um projeto com GUID = {guid_projeto}"
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
            Captura os projetos que o usu??rio
            marcou como seu interesse
        """
        return await self.proj_repo.get_projetos_interesse_usuario(guid_usuario)

    @staticmethod
    def build_interesse_usuario_projeto_filters(
            fl_usuario_interesse: Optional[bool] = None,
            fl_projeto_interesse: Optional[bool] = None,
            fl_match: Optional[bool] = None
    ) -> List:
        filters = []

        if fl_usuario_interesse is not None:
            filters.append(InteresseUsuarioProjeto.fl_usuario_interesse == fl_usuario_interesse)

        if fl_projeto_interesse is not None:
            filters.append(InteresseUsuarioProjeto.fl_projeto_interesse == fl_projeto_interesse)

        if fl_match is not None:
            filters.append(InteresseUsuarioProjeto.fl_match == fl_match)

        return filters

    async def get_usuarios_interessados_projeto_by_filtros(
            self, guid_projeto: str, fl_usuario_interesse: Optional[bool] = None,
            fl_projeto_interesse: Optional[bool] = None,
            fl_match: Optional[bool] = None
    ) -> List[InteresseUsuarioProjeto]:
        """
            Captura os usu??rios interessados pelo projeto ou que o projeto
            est?? interessado

            Podem ser adicionados filtros:

            - fl_usuario_interesse: Interesse do usu??rio pelo projeto
            - fl_projeto_interesse: Interesse do projeto pelo usu??rio
            - fl_match: Match entre ambos
        """

        filters = self.build_interesse_usuario_projeto_filters(fl_usuario_interesse, fl_projeto_interesse, fl_match)
        return await self.proj_repo.get_usuarios_interessados_projeto(guid_projeto, filters)

    async def get_projetos_interesse_usuario_by_filtros(
            self, guid_usuario: str, fl_usuario_interesse: Optional[bool] = None,
            fl_projeto_interesse: Optional[bool] = None,
            fl_match: Optional[bool] = None
    ):
        """
            Captura os projetos que o usu??rio
            marcou como seu interesse ou
            projeto marcou o usuario como interesse

            Podem ser adicionados filtros:

            - fl_usuario_interesse: Interesse do usu??rio pelo projeto
            - fl_projeto_interesse: Interesse do projeto pelo usu??rio
            - fl_match: Match entre ambos
        """

        filters = self.build_interesse_usuario_projeto_filters(fl_usuario_interesse, fl_projeto_interesse, fl_match)
        return await self.proj_repo.get_projetos_interesse_usuario(guid_usuario, filters)

    async def get_projetos_usuario(self, guid_usuario: str):
        """
            Captura os projetos que o usu??rio
            pertence com algum v??nculo de fun????o no projeto
        """
        return await self.proj_repo.get_projetos_usuario(guid_usuario)
