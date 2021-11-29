from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Optional
from typing import List

from server.services.projetos_service import ProjetosService
from server.services.relacao_projeto_tag_service import RelacaoProjetoTagService
from server.schemas.relacao_projeto_tag_schema import RelacaoProjetoTagInput, RelacaoProjetoTagOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.projetos_repository import ProjetoRepository


router = APIRouter()

rel_projeto_tag_router = dict(
    router=router,
    tags=["Relação projeto tag"],
)


@cbv(router)
class RelacaoProjetoTagController:
    @router.post(path="/rel_projeto_tag", response_model=List[RelacaoProjetoTagOutput])
    @endpoint_exception_handler
    async def post_rel_projeto_tag(self, data: List[RelacaoProjetoTagInput],
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = RelacaoProjetoTagService(
            ProjetoRepository(session, environment),
            environment
        )

        return await service.create(data)

    @router.delete(path="/rel_projeto_tag/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_rel_projeto_tag(self, data: List[RelacaoProjetoTagInput],
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = RelacaoProjetoTagService(
            ProjetoRepository(session, environment),
            environment
        )
        await service.delete(data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
