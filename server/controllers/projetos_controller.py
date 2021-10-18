from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.projetos_service import ProjetosService
from server.schemas.projetos_schema import ProjetosOutput, ProjetosInput


router = APIRouter()
projetos_router = dict(
    router=router,
    prefix="/projetos",
    tags=["projetos"],
)

class ProjetosController:
    @router.get(path="", response_model=List[ProjetosOutput])
    async def get_projetos(self, id: Optional[int] = None, guid: Optional[str] = None):
        service = ProjetosService()
        return await service.get(id=id, guid=guid)

    @router.post(path="", response_model=List[ProjetosOutput])
    async def post_projetos(self, data: List[ProjetosInput]):
        service = ProjetosService()
        return await service.create(data)

    @router.put(path="", response_model=List[ProjetosOutput])
    async def put_projetos(self, data: List[ProjetosInput]):
        service = ProjetosService()
        return await service.update(data)

    @router.delete(path="/{guid}", response_model=List[ProjetosOutput])
    async def delete_projetos(self, guid: str):
        service = ProjetosService()
        return await service.delete(guid)
