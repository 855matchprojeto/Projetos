from fastapi import APIRouter, Depends, Security
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List
from server.services.relacao_projeto_usuario import RelacaoProjetoUsuarioService
from server.schemas.relacao_projeto_usuario_schema import RelacaoProjetoUsuarioInput, RelacaoProjetoUsuarioOutput
from server.schemas import usuario_schema
from server.dependencies.get_current_user import get_current_user

router = APIRouter()
relacao_projeto_usuario_router = dict(
    router=router,
    prefix="/relacao_projeto_usuario",
    tags=["Relação Projeto Usuário"],
)


class RelacaoProjetoUsuarioController:
    @router.get(path="/relacao_projeto_usuario", response_model=List[RelacaoProjetoUsuarioOutput])
    async def get_rel_projeto_usuario(self, id: Optional[int] = None, guid: Optional[str] = None,
                                      current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                               scopes=[])):
        """
        Endpoint para pegar todas as relações entre projetos e usuários
        Args:
            id: (optional) id do histórico
            guid: (optional) guid do histórico
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - lista com relações entre projetos e usuários
        """
        service = RelacaoProjetoUsuarioService()
        return await service.get(id=id, guid=guid)

    @router.post(path="/relacao_projeto_usuario", response_model=List[RelacaoProjetoUsuarioOutput])
    async def post_rel_projeto_usuario(self, data: List[RelacaoProjetoUsuarioInput],
                                       current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                                scopes=[])):
        """
        Endpoint para criar uma relação entre projeto e usuário
        Args:
            data: relação entre projeto e usuário a ser criada
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - relação criada entre projeto e usuário
        """
        service = RelacaoProjetoUsuarioService()
        return await service.create(data)

    @router.put(path="/relacao_projeto_usuario", response_model=List[RelacaoProjetoUsuarioOutput])
    async def put_rel_projeto_usuario(self, data: List[RelacaoProjetoUsuarioInput],
                                      current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                               scopes=[])):
        """
        Endpoint para atualizar uma relação entre projeto e usuário
        Args:
            data: relação entre projeto e usuário a ser atualizada
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - relação atualizada entre projeto e usuário
        """
        service = RelacaoProjetoUsuarioService()
        return await service.update(data)

    @router.delete(path="/relacao_projeto_usuario/{guid}", response_model=List[RelacaoProjetoUsuarioOutput])
    async def delete_rel_projeto_usuario(self, guid: str,
                                         current_user: usuario_schema.CurrentUserToken = Security(get_current_user,
                                                                                                  scopes=[])):
        """
        Endpoint para deletar uma relação entre projeto e usuário
        Args:
            data: relação entre projeto e usuário a ser deletada
            current_user: usuário fazendo a requisição

        Returns:
            código 204 (no content)
        """
        service = RelacaoProjetoUsuarioService()
        return await service.delete(guid)
