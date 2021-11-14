from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.funcoes_projeto_service import FuncoesProjetoService
from server.schemas.funcao_projeto_schema import FuncaoProjetosInput, FuncaoProjetosOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.funcoes_projeto_repository import FuncoesProjetoRepository


router = APIRouter()

funcao_projeto_router = dict(
    router=router,
    tags=["Função Projeto"],
)


@cbv(router)
class FuncaoProjetosController:
    @router.get("/funcoes", response_model=List[FuncaoProjetosOutput])
    @endpoint_exception_handler
    async def get_funcoes_projeto(self, id: Optional[int] = None, guid: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        service = FuncoesProjetoService(
            FuncoesProjetoRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/funcoes", response_model=FuncaoProjetosOutput)
    @endpoint_exception_handler
    async def post_funcao_projeto(self, data: FuncaoProjetosInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = FuncoesProjetoService(
            FuncoesProjetoRepository(session, environment),
            environment
        )
        return await service.create(data)


    @router.put(path="/funcoes/{guid}", response_model=FuncaoProjetosOutput)
    @endpoint_exception_handler
    async def put_funcao_projeto(self, guid, data: FuncaoProjetosInput,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = FuncoesProjetoService(
            FuncoesProjetoRepository(session, environment),
            environment
        )
        return await service.update_by_guid(guid=guid, funcao_input=data)

    @router.delete(path="/funcoes/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_funcao_projeto(self, guid: str,
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = FuncoesProjetoService(
            FuncoesProjetoRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
