from fastapi import APIRouter, Depends, Security
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.dependencies.session import get_session
from server.repository.historico_projetos_repository import HistoricoProjetoRepository
from server.services.historico_projetos_service import HistoricoProjetosService
from server.schemas.historico_projetos_schema import HistoricoProjetosInput, HistoricoProjetosOutput
from server.schemas import usuario_schema
from server.dependencies.get_current_user import get_current_user

router = APIRouter()
historico_projetos_router = dict(
    router=router,
    tags=["Histórico Projetos"],
)

@cbv(router)
class HistoricoProjetosController:
    @router.get(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def get_historico_projetos(self, id: Optional[int] = None, guid: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):

        service = HistoricoProjetosService(
            HistoricoProjetoRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def post_historico_projetos(self, data: List[HistoricoProjetosInput],
                                      current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                               scopes=[])):
        service = HistoricoProjetosService()
        return await service.create(data)

    @router.put(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def put_historico_projetos(self, data: List[HistoricoProjetosInput],
                                     current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                              scopes=[])):
        service = HistoricoProjetosService()
        return await service.update(data)

    @router.delete(path="/historico_projetos/{guid}", response_model=List[HistoricoProjetosOutput])
    async def delete_historico_projetos(self, guid: str,
                                        current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                                 scopes=[])):
        service = HistoricoProjetosService()
        return await service.delete(guid)
