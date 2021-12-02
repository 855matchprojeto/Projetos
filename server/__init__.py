from fastapi import FastAPI
from server.configuration import exceptions
from server.controllers.usuario_controller import usuario_router
from server.controllers.ping_controller import ping_router
from server.controllers.projetos_controller import projetos_router
from server.controllers.funcao_projetos_controller import funcao_projeto_router
from server.controllers.historico_projetos_controller import historico_projetos_router
from server.controllers.relacao_projeto_usuario_controller import relacao_projeto_usuario_router
from server.controllers.relacao_projeto_tag_controller import rel_projeto_tag_router
from server.controllers.relacao_projeto_entidade_controller import rel_projeto_entidade_router
from server.controllers.tag_controller import tag_router
from server.controllers.interesse_controller import interesse_router

from server.controllers.tipo_tag_controller import tipo_tag_router
from server.controllers.entidade_externa_controller import entidade_externa_router
from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins
from server.configuration.custom_logging import MICROSERVICE_LOGGER_KWARGS, Logger
from server.middleware.plugins import custom_request_plugin
from server.configuration import db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from server.controllers.curso_controller import curso_router
from server.controllers.relacao_projeto_curso_controller import rel_projeto_curso_router
from server.controllers.relacao_projeto_interesse_controller import rel_projeto_interesse_router


routers = [
    usuario_router,
    ping_router,
    projetos_router,
    funcao_projeto_router,
    historico_projetos_router,
    relacao_projeto_usuario_router,
    tag_router,
    tipo_tag_router,
    entidade_externa_router,
    rel_projeto_tag_router,
    rel_projeto_entidade_router,
    interesse_router,
    curso_router,
    rel_projeto_interesse_router,
    rel_projeto_curso_router
]


def _init_app():
    app = FastAPI()
    app = configura_exception_handlers(app)
    app = configura_middlewares(app)
    configura_logger()
    configura_routers(app)
    return app


def configura_logger():
    Logger(**MICROSERVICE_LOGGER_KWARGS).get_logger()


def configura_middlewares(app):
    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            custom_request_plugin.RequestPlugin()
        )
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    return app


def configura_exception_handlers(app):
    app.add_exception_handler(
        exceptions.ApiBaseException,
        exceptions.api_base_exception_handler
    )
    app.add_exception_handler(
        exceptions.InvalidEmailException,
        exceptions.api_base_exception_handler
    ),
    app.add_exception_handler(
        RequestValidationError,
        exceptions.request_validation_error_handler
    )
    app.add_exception_handler(
        Exception,
        exceptions.generic_exception_handler
    )
    return app


def configura_routers(app):
    for router in routers:
        app.include_router(**router),

