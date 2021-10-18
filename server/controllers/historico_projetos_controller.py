from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.historico_projetos_service import HistoricoProjetosService
from server.schemas.historico_projetos_schema import HistoricoProjetosInput, HistoricoProjetosOutput

router = APIRouter()
historico_projetos_router = dict(
    router=router,
    prefix="/historico_projetos",
    tags=["Histórico Projetos"],
)

class Funcoes_ProjetoController:
    @router.get(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def get_historico_projetos(self, id: Optional[int] = None, guid: Optional[str] = None):
        service = HistoricoProjetosService()
        return await service.get(id=id, guid=guid)

    @router.post(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def post_historico_projetos(self, data: List[HistoricoProjetosInput]):
        service = HistoricoProjetosService()
        return await service.create(data)

    @router.put(path="/historico_projetos", response_model=List[HistoricoProjetosOutput])
    async def put_historico_projetos(self, data: List[HistoricoProjetosInput]):
        service = HistoricoProjetosService()
        return await service.update(data)

    @router.delete(path="/historico_projetos/{guid}", response_model=List[HistoricoProjetosOutput])
    async def delete_historico_projetos(self, guid: str):
        service = HistoricoProjetosService()
        return await service.delete(guid)





