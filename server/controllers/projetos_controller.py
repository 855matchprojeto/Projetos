from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List

from server.repository.historico_projetos_repository import HistoricoProjetoRepository
from server.services.historico_projetos_service import HistoricoProjetosService
from server.services.projetos_service import ProjetosService
from server.schemas.projetos_schema import ProjetosOutput, ProjetosInput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.projetos_repository import ProjetoRepository


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
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/projetos", response_model=ProjetosOutput)
    @endpoint_exception_handler
    async def post_projetos(self, data: ProjetosInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )

        hist_service = HistoricoProjetosService(
            HistoricoProjetoRepository(session, environment),
            environment
        )

        await hist_service.create(data)
        return await service.create(data)

    @router.post(path="/projeto_completo", response_model=ProjetosOutput)
    @endpoint_exception_handler
    async def post_projeto_completo(self, data: ProjetosInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )

        hist_service = HistoricoProjetosService(
            HistoricoProjetoRepository(session, environment),
            environment
        )

        await hist_service.create(data)
        data = await service.create(data)
        return data;


    @router.put(path="/projetos/{guid}", response_model=ProjetosOutput)
    @endpoint_exception_handler
    async def put_projetos(self, guid, data: ProjetosInput,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
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
        service = ProjetosService(
            ProjetoRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
