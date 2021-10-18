from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.relacao_projeto_usuario import RelacaoProjetoUsuarioService
from server.schemas.relacao_projeto_usuario_schema import HistoricoProjetosInput, HistoricoProjetosOutput

router = APIRouter()
relacao_projeto_usuario_router = dict(
    router=router,
    prefix="/relacao_projeto_usuario",
    tags=["Relação Projeto Usuário"],
)

class HistoricoProjetosController:
    @router.get(path="/relacao_projeto_usuario", response_model=List[HistoricoProjetosOutput])
    async def get_rel_projeto_usuario(self, id: Optional[int] = None, guid: Optional[str] = None):
        service = RelacaoProjetoUsuarioService()
        return await service.get(id=id, guid=guid)

    @router.post(path="/relacao_projeto_usuario", response_model=List[HistoricoProjetosOutput])
    async def post_rel_projeto_usuario(self, data: List[HistoricoProjetosInput]):
        service = RelacaoProjetoUsuarioService()
        return await service.create(data)

    @router.put(path="/relacao_projeto_usuario", response_model=List[HistoricoProjetosOutput])
    async def put_rel_projeto_usuario(self, data: List[HistoricoProjetosInput]):
        service = RelacaoProjetoUsuarioService()
        return await service.update(data)

    @router.delete(path="/relacao_projeto_usuario/{guid}", response_model=List[HistoricoProjetosOutput])
    async def delete_rel_projeto_usuario(self, guid: str):
        service = RelacaoProjetoUsuarioService()
        return await service.delete(guid)





