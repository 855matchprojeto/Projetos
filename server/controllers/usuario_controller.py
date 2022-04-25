from server.schemas import usuario_schema
from server.services.usuario_service import UsuarioService
from server.dependencies.session import get_session
from server.dependencies.get_environment_cached import get_environment_cached
from server.configuration.db import AsyncSession
from server.controllers import endpoint_exception_handler
from typing import List, Optional
from server.dependencies.get_current_user import get_current_user
from server.configuration.environment import Environment
from server.schemas import error_schema
from server.services.projetos_service import ProjetosService
from server.repository.projetos_repository import ProjetoRepository
from server.schemas.interesse_usuario_projeto_schema import InteresseUsuarioProjetoOutput, InteresseUsuarioProjetoInput
from fastapi import APIRouter, Depends, Security, status, Response
from server.schemas.projetos_schema import SimpleProjetosOutput
from server.dependencies.get_sns_publisher_service import get_sns_publisher_service
from server.services.aws_publisher_service import AWSPublisherService


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
    response_model=List[SimpleProjetosOutput],
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


@router.get(
    "/me/projects/user-project-interest",
    tags=[
        "Projetos",
        "InteresseUsuarioProjeto"
    ],
    response_model=List[SimpleProjetosOutput],
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
async def get_current_user_projects_interested_by_filtros(
    fl_usuario_interesse: Optional[bool] = None,
    fl_projeto_interesse: Optional[bool] = None,
    fl_match: Optional[bool] = None,
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
    return await projetos_service.get_projetos_interesse_usuario_by_filtros(
        guid_curr_user, fl_usuario_interesse, fl_projeto_interesse, fl_match
    )


@router.get(
    "/me/projects",
    tags=[
        "Projetos"
    ],
    response_model=List[SimpleProjetosOutput],
    summary='Retorna os projetos em que o usuário pertence',
    response_description='Retorna os projetos em que o usuário pertence',
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
async def get_current_user_projects(
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
):

    """
        # Descrição

        Retorna os projetos que o usuário pertence

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
    return await projetos_service.get_projetos_usuario(guid_curr_user)


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
    publisher_service: AWSPublisherService = Depends(get_sns_publisher_service)
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
        environment=environment,
        publisher_service=publisher_service
    )

    return await projetos_service.insert_interesse_usuario_projeto(
        current_user, guid_projeto
    )


@router.put(
    "/user/{guid_usuario}/project/{guid_projeto}/user-project-interest",
    tags=[
        "Projetos",
        "InteresseUsuarioProjeto"
    ],
    response_model=InteresseUsuarioProjetoOutput,
    summary='Insere ou atualiza a tabela que relaciona interesses de usuário pelo projeto ou projeto pelo usuário',
    response_description=f'Corpo da relação da tabela que relaciona interesses de usuário'
                         f' pelo projeto ou projeto pelo usuário',
    responses={
        401: {
            'model': error_schema.ErrorOutput401,
        },
        404: {
            'model': error_schema.ErrorOutput404,
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
async def upsert_user_project_interest(
    guid_usuario: str, guid_projeto: str,
    input_body: InteresseUsuarioProjetoInput,
    _: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
    publisher_service: AWSPublisherService = Depends(get_sns_publisher_service)
):

    """
        # Descrição

        **Insere ou atualiza** a tabela que relaciona interesses de usuário pelo projeto ou projeto pelo usuário.
        O corpo da requisição é composto dos seguiintes campos:

        - fl_usuario_interesse: Interesse de usuário pelo projeto
        - fl_projeto_interesse: Interesse de projeto pelo usuário

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
        environment=environment,
        publisher_service=publisher_service
    )

    return await projetos_service.upsert_interesse_usuario_projeto(
        guid_usuario, guid_projeto, input_body
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

