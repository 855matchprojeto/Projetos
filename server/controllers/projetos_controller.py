from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List

from server.repository.historico_projetos_repository import HistoricoProjetoRepository
from server.repository.relacao_projeto_entidade_repository import RelacaoProjetoEntidadeRepository
from server.repository.relacao_projeto_tag_repository import RelacaoProjetoTagRepository
from server.services.historico_projetos_service import HistoricoProjetosService
from server.services.projetos_service import ProjetosService
from server.services.relacao_projeto_entidade_service import RelacaoProjetoEntidadeService
from server.services.relacao_projeto_tag_service import RelacaoProjetoTagService
from server.schemas.projetos_schema import ProjetosOutput, ProjetosInput, ProjetosInputUpdate
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.projetos_repository import ProjetoRepository
from server.repository.funcoes_projeto_repository import FuncoesProjetoRepository
from server.services.relacao_projeto_curso_service import RelacaoProjetoCursoService
from server.services.relacao_projeto_interesse_service import RelacaoProjetoInteresseService
from server.repository.relacao_projeto_curso_repository import RelacaoProjetoCursoRepository
from server.repository.relacao_projeto_interesse_repository import RelacaoProjetoInteresseRepository
from server.schemas.interesse_usuario_projeto_schema import InteresseUsuarioProjetoOutput
from server.schemas import error_schema


router = APIRouter()

projetos_router = dict(
    router=router,
    tags=["projetos"],
)


@cbv(router)
class ProjetosController:
    @router.get("/projetos", response_model=List[ProjetosOutput])
    @endpoint_exception_handler
    async def get_projetos(self, id: Optional[int] = None, guid: Optional[str] = None,
                           titulo_ilike: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        """
        Endpoint para pegar todos os projetos
        Args:
            id: (optional) id do histórico
            guid: (optional) guid do histórico
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - lista com projetos
        """
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid, titulo_ilike=titulo_ilike)

    @router.post(path="/projetos", response_model=ProjetosOutput)
    @endpoint_exception_handler
    async def post_projetos(self, data: ProjetosInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para criar um projeto
        Args:
            data: projeto a ser criado
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - projeto criado
        """
        data = data.convert_to_dict()
        if data["tags"]:
            tags = data["tags"]
        else:
            tags = []
        if data["entidades"]:
            entidades = data["entidades"]
        else:
            entidades = []
        if data["cursos"]:
            cursos = data["cursos"]
        else:
            cursos = []
        if data["interesses"]:
            interesses = data["interesses"]
        else:
            interesses = []
        del data["tags"]
        del data["entidades"]
        del data["cursos"]
        del data["interesses"]

        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment,
            FuncoesProjetoRepository(session, environment)
        )
        # criando também o histórico
        hist_service = HistoricoProjetosService(
            HistoricoProjetoRepository(session, environment),
            environment
        )
        # relação projeto entidade externa
        rel_entidade_service = RelacaoProjetoEntidadeService(
            RelacaoProjetoEntidadeRepository(session, environment),
            environment
        )
        # relação projeto tag
        rel_tag_service = RelacaoProjetoTagService(
            RelacaoProjetoTagRepository(session, environment),
            environment
        )
        # relação projeto curso
        rel_curso_service = RelacaoProjetoCursoService(
            RelacaoProjetoCursoRepository(session, environment),
            environment
        )
        # relação projeto interesse
        rel_interesse_service = RelacaoProjetoInteresseService(
            RelacaoProjetoInteresseRepository(session, environment),
            environment
        )
        guid_usuario = current_user.guid
        await hist_service.create(data)
        projeto = await service.create(data, guid_usuario)
        if entidades:
            data_entidade = []
            for entidade in entidades:
                data = {'id_projetos': projeto.id, 'id_entidade': entidade}
                # rel_entidade = await rel_entidade_service.create(data)
                data_entidade.append({'id_projetos': projeto.id, 'id_entidade': entidade})
            rel_entidade = await rel_entidade_service.mult_insert(data_entidade)

        if tags:
            data_tags = []
            for tag in tags:
                data_tags.append({'id_projetos': projeto.id, 'id_tags': tag})
            rel_tag = await rel_tag_service.mult_insert(data_tags)

        if cursos:
            data_cursos = []
            for curso in cursos:
                data_cursos.append({'id_projetos': projeto.id, 'id_cursos': curso})
            rel_curso = await rel_curso_service.mult_insert(data_cursos)

        if interesses:
            data_interesses = []
            for interesse in interesses:
                data_interesses.append({'id_projetos': projeto.id, 'id_interesses': interesse})
            rel_interesse = await rel_interesse_service.mult_insert(data_interesses)

        return projeto

    @router.put(path="/projetos/{guid}", response_model=ProjetosOutput)
    @endpoint_exception_handler
    async def put_projetos(self, guid, data: ProjetosInputUpdate,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para atualizar um projeto
        Args:
            data: projeto a ser atualizado
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - projeto atualizado
        """
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )
        return await service.update_by_guid(guid=guid, projeto_input=data)

    @router.delete(path="/projetos/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_projetos(self, guid: str,
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para deletar um projeto
        Args:
            guid: guid do projeto
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 204 (no content)
        """
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.get(
        "/projects/{guid_projeto}/user-project-interest",
        tags=[
            "Projetos",
            "InteresseUsuarioProjeto"
        ],
        response_model=List[InteresseUsuarioProjetoOutput],
        summary='Retorna os usuários com interesse pelo projeto ou no qual o projeto está interessado',
        response_description=f'Retorna os usuários com interesse pelo projeto ou no qual o projeto está interessado. Note que' \
                             f'são retornados os usuários a partir da tabela "InteresseUsuarioProjeto". Para capturar informações' \
                             f'de perfil será necessário realizar uma requisição para outro microserviço',
        responses={
            401: {
                'model': error_schema.ErrorOutput401,
            },
            422: {
                'model': error_schema.ErrorOutput422,
            },
            500: {
                'model': error_schema.ErrorOutput500
            }
        }
    )
    @endpoint_exception_handler
    async def get_usuarios_interessados_projeto_by_filtros(
        self, guid_projeto: str,
        fl_usuario_interesse: Optional[bool] = None,
        fl_projeto_interesse: Optional[bool] = None,
        fl_match: Optional[bool] = None,
        _: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
        session: AsyncSession = Depends(get_session),
        environment: Environment = Depends(get_environment_cached),
    ):

        """
            # Descrição

            Retorna os projetos que o usuário marcou como de seu interesse

            # Erros

            Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

            - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
            - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
            no formato de string, contendo os erros de validação encontrados.
            - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema

        """

        projetos_service = ProjetosService(
            proj_repo=ProjetoRepository(session, environment),
            environment=environment
        )

        return await projetos_service.get_usuarios_interessados_projeto_by_filtros(
            guid_projeto, fl_usuario_interesse, fl_projeto_interesse, fl_match
        )
