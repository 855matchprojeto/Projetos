from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.funcoes_projeto_service import FuncoesProjetoService
from server.schemas.funcao_projeto_schema import FuncaoProjetosInput, FuncaoProjetosOutput

router = APIRouter()
funcao_projeto_router = dict(
    router=router,
    prefix="/Funcoes_projeto",
    tags=["Funções Projetos"],
)

class Funcoes_ProjetoController:
    @router.get(path="", response_model=List[FuncaoProjetosOutput])
    async def get_funcoes(self, id: Optional[int] = None, guid: Optional[str] = None):
        service = FuncoesProjetoService()
        return await service.get(id=id, guid=guid)

    @router.post(path="", response_model=List[FuncaoProjetosOutput])
    async def post_funcoes(self, data: List[FuncaoProjetosInput]):
        service = FuncoesProjetoService()
        return await service.create(data)

    @router.put(path="", response_model=List[FuncaoProjetosOutput])
    async def put_funcoes(self, data: List[FuncaoProjetosInput]):
        service = FuncoesProjetoService()
        return await service.update(data)

    @router.delete(path="/{guid}", response_model=List[FuncaoProjetosOutput])
    async def delete_funcoes(self, guid: str):
        service = FuncoesProjetoService()
        return await service.delete(guid)





