from fastapi import APIRouter, Depends, Security
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.historico_projetos_service import HistoricoProjetosService
from server.schemas.historico_projetos_schema import HistoricoProjetosInput, HistoricoProjetosOutput
from server.schemas import usuario_schema
from server.dependencies.get_current_user import get_current_user

router = APIRouter()
historico_projetos_router = dict(
    router=router,
    prefix="/historico_projetos",
    tags=["Histórico Projetos"],
)


class Funcoes_ProjetoController:
    @router.get(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def get_historico_projetos(self, id: Optional[int] = None, guid: Optional[str] = None,
                                     current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                              scopes=[])):
        service = HistoricoProjetosService()
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
