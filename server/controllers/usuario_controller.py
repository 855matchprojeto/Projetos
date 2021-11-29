from server.schemas import usuario_schema, token_shema
from server.services.usuario_service import UsuarioService
from server.dependencies.session import get_session
from server.dependencies.get_environment_cached import get_environment_cached
from server.configuration.db import AsyncSession
from fastapi import Depends, Security
from server.controllers import endpoint_exception_handler
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from server.dependencies.get_current_user import get_current_user
from server.constants.permission import RoleBasedPermission
from server.configuration.environment import Environment
from server.schemas import error_schema
from server.services.projetos_service import ProjetosService
from server.repository.projetos_repository import ProjetoRepository
from server.schemas.interesse_usuario_projeto_schema import InteresseUsuarioProjetoOutput
from fastapi import APIRouter, Depends, Security, status, Response
from server.schemas.projetos_schema import ProjetosOutput


router = APIRouter()
usuario_router = dict(
    router=router,
    prefix="/users",
    tags=["Usuários"],
)


@router.get(
    "/me",
    response_model=usuario_schema.CurrentUserOutput,
    summary='Retorna as informações contidas no token do usuário',
    response_description='Informações contidas no token do usuário',
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
async def get_current_user(
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
):

    """
        # Descrição

        Retorna as informações do usuário atual vinculadas ao token.

        # Erros

        Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

        - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
        - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
        no formato de string, contendo os erros de validação encontrados.
        - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema

    """

    return UsuarioService.current_user_output(current_user)


@router.get(
    "/me/projects/interested-in",
    tags=[
        "Projetos",
        "InteresseUsuarioProjeto"
    ],
    response_model=List[ProjetosOutput],
    summary='Retorna os projetos que o usuário marcou como de seu interesse',
    response_description='Retorna os projetos que o usuário marcou como de seu interesse',
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
async def get_current_user_projects_interested(
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
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

    guid_curr_user = current_user.guid
    return await projetos_service.get_projetos_interesse_usuario(guid_curr_user)


@router.post(
    "/me/project/{guid_projeto}/user-project-interest",
    tags=[
        "Projetos",
        "InteresseUsuarioProjeto"
    ],
    response_model=InteresseUsuarioProjetoOutput,
    summary='Vincula um projeto como um interesse do usuário atual',
    response_description='Vincula um projeto como um interesse do usuário atual',
    responses={
        401: {
            'model': error_schema.ErrorOutput401,
        },
        404: {
            'model': error_schema.ErrorOutput404
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
async def link_project_as_current_user_interest(
    guid_projeto: str,
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
):

    """
        # Descrição

        Vincula um projeto como um interesse do usuário atual

        # Erros

        Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

        - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
        - **(PROJECT_NOT_FOUND, 404)**: Projeto não encontrado com o GUID solicitado.
        - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
        no formato de string, contendo os erros de validação encontrados.
        - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema

    """

    projetos_service = ProjetosService(
        proj_repo=ProjetoRepository(session, environment),
        environment=environment
    )

    guid_curr_user = current_user.guid
    return await projetos_service.insert_interesse_usuario_projeto(
        guid_curr_user, guid_projeto
    )


@router.delete(
    "/me/project/{guid_projeto}/user-project-interest",
    tags=[
        "Projetos",
        "InteresseUsuarioProjeto"
    ],
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Vincula um projeto como um interesse do usuário atual',
    responses={
        401: {
            'model': error_schema.ErrorOutput401,
        },
        404: {
            'model': error_schema.ErrorOutput404
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
async def unlink_project_current_user_interest(
    guid_projeto: str,
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
):

    """
        # Descrição

        Desvincula um projeto como um interesse do usuário atual, removendo a entidade
        de ligação

        # Erros

        Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

        - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
        - **(PROJECT_NOT_FOUND, 404)**: Projeto não encontrado com o GUID solicitado.
        - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
        no formato de string, contendo os erros de validação encontrados.
        - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema

    """

    projetos_service = ProjetosService(
        proj_repo=ProjetoRepository(session, environment),
        environment=environment
    )

    guid_curr_user = current_user.guid
    await projetos_service.delete_interesse_usuario_projeto(
        guid_curr_user, guid_projeto
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

