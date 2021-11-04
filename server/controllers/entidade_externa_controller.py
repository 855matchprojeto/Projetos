from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from typing import Optional
from typing import List
from server.services.entidade_externa_service import EntidadeExternaService
from server.schemas.entidade_externa_schema import EntidadeExternaInput, EntidadeExternaOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.entidade_externa_repository import EntidadeExternaRepository


router = APIRouter()

entidade_externa_router = dict(
    router=router,
    tags=["Entidade externa"],
)


@cbv(router)
class TagController:
    @router.get("/entidade_externa", response_model=List[EntidadeExternaOutput])
    @endpoint_exception_handler
    async def get_tags(self, id: Optional[int] = None, guid: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        service = EntidadeExternaService(
            EntidadeExternaRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/entidade_externa", response_model=EntidadeExternaOutput)
    @endpoint_exception_handler
    async def post_tag(self, data: EntidadeExternaInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = EntidadeExternaService(
            EntidadeExternaRepository(session, environment),
            environment
        )
        return await service.create(data)


    @router.put(path="/entidade_externa/{guid}", response_model=EntidadeExternaOutput)
    @endpoint_exception_handler
    async def put_tag(self, guid, data: EntidadeExternaInput,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = EntidadeExternaService(
            EntidadeExternaRepository(session, environment),
            environment
        )
        return await service.update_by_guid(guid=guid, tipo_tag_input=data)

    @router.delete(path="/entidade_externa/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_tag(self, guid: str,
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        service = EntidadeExternaService(
            EntidadeExternaRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
