from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from typing import Optional
from typing import List
from server.services.interesse_service import InteresseService
from server.schemas.interesse_schema import InteresseInput, InteresseOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.interesse_repository import InteresseRepository


router = APIRouter()

interesse_router = dict(
    router=router,
    tags=["Interesse"],
)


@cbv(router)
class InteresseController:
    @router.get("/interesse", response_model=List[InteresseOutput])
    @endpoint_exception_handler
    async def get_interesse(self, id: Optional[int] = None, guid: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        """
        Endpoint para pegar todas as interesse
        Args:
            id: (optional) id do interesse
            guid: (optional) guid do interesse
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - lista com interesses
        """
        service = InteresseService(
            InteresseRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/interesse", response_model=InteresseOutput)
    @endpoint_exception_handler
    async def post_interesse(self, data: InteresseInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para criar um novo interesse
        Args:
            data: interesse a ser criado
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - interesse criado
        """
        service = InteresseService(
            InteresseRepository(session, environment),
            environment
        )
        return await service.create(data)


    @router.put(path="/interesse/{guid}", response_model=InteresseOutput)
    @endpoint_exception_handler
    async def put_interesse(self, guid, data: InteresseInput,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para atualizar um interesse pelo guid
        Args:
            guid: guid do interesse
            data: interesse a ser modificada
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - interesse atualizado
        """
        service = InteresseService(
            InteresseRepository(session, environment),
            environment
        )
        return await service.update_by_guid(guid=guid, interesse_input=data)

    @router.delete(path="/interesse/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_interesse(self, guid: str,
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para deletar um interesse
        Args:
            guid: guid do interesse
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 204 (no content)
        """
        service = InteresseService(
            InteresseRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
