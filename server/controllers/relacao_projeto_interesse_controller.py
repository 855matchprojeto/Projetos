from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from typing import Optional
from typing import List

from server.services.relacao_projeto_interesse_service import RelacaoProjetoInteresseService
from server.schemas.relacao_projeto_interesse_schema import RelacaoProjetoInteresseInput, RelacaoProjetoInteresseOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.relacao_projeto_interesse_repository import RelacaoProjetoInteresseRepository


router = APIRouter()

rel_projeto_interesse_router = dict(
    router=router,
    tags=["Relação projeto interesse"],
)


@cbv(router)
class RelacaoProjetoInteresseController:
    @router.get("/rel_projeto_interesse", response_model=List[RelacaoProjetoInteresseOutput])
    @endpoint_exception_handler
    async def get_rel_projeto_interesse(self, id_projetos: Optional[int] = None, id_interesses: Optional[int] = None,
                       session: AsyncSession = Depends(get_session),
                       environment: Environment = Depends(get_environment_cached),
                       current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                       ):
        service = RelacaoProjetoInteresseService(
            RelacaoProjetoInteresseRepository(session, environment),
            environment
        )
        return await service.get(id_projetos=id_projetos, id_interesses=id_interesses)


    @router.post(path="/rel_projeto_interesse", response_model=List[RelacaoProjetoInteresseOutput])
    @endpoint_exception_handler
    async def post_rel_projeto_interesse(self, data: List[RelacaoProjetoInteresseInput],
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = RelacaoProjetoInteresseService(
            RelacaoProjetoInteresseRepository(session, environment),
            environment
        )

        resp = await service.mult_insert(data)
        return resp

    @router.delete(path="/rel_projeto_interesse", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_rel_projeto_interesse(self, data: List[RelacaoProjetoInteresseInput],
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = RelacaoProjetoInteresseService(
            RelacaoProjetoInteresseRepository(session, environment),
            environment
        )
        await service.mult_delete(data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
