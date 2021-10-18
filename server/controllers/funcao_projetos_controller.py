from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.funcoes_projeto_service import FuncoesProjetoService
from server.schemas.funcao_projeto_schema import FuncaoProjetosInput, FuncaoProjetosOutput

router = InferringRouter(tags=["Função Projeto"])

@cbv(router)
class Funcoes_ProjetoController:
    @router.get(path="/Funcoes_projeto", response_model=List[FuncaoProjetosOutput])
    async def get_funcoes(self, id: Optional[int] = None, guid: Optional[str] = None):
        service = FuncoesProjetoService()
        return await service.get(id=id, guid=guid)

    @router.post(path="/Funcoes_projeto", response_model=List[FuncaoProjetosOutput])
    async def post_funcoes(self, data: List[FuncaoProjetosInput]):
        service = FuncoesProjetoService()
        return await service.create(data)

    @router.put(path="/Funcoes_projeto", response_model=List[FuncaoProjetosOutput])
    async def put_funcoes(self, data: List[FuncaoProjetosInput]):
        service = FuncoesProjetoService()
        return await service.update(data)

    @router.delete(path="/Funcoes_projeto/{guid}", response_model=List[FuncaoProjetosOutput])
    async def delete_funcoes(self, guid: str):
        service = FuncoesProjetoService()
        return await service.delete(guid)





