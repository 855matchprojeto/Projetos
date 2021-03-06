from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from typing import Optional
from typing import List
from server.services.tipo_tag_service import TipoTagService
from server.schemas.tipo_tag_schema import TipoTagInput, TipoTagOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.tipo_tag_repository import TipoTagRepository


router = APIRouter()

tipo_tag_router = dict(
    router=router,
    tags=["Tipo de Tags"],
)


@cbv(router)
class TagController:
    @router.get("/tipo_tags", response_model=List[TipoTagOutput])
    @endpoint_exception_handler
    async def get_tags(self, id: Optional[int] = None, guid: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        """
        Endpoint para pegar todos os tipos de tags
        Args:
            id: (optional) id do tipo de tag
            guid: (optional) guid do tipo de tag
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - lista com tipos de tags
        """
        service = TipoTagService(
            TipoTagRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/tipo_tags", response_model=TipoTagOutput)
    @endpoint_exception_handler
    async def post_tag(self, data: TipoTagInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para criar um tipo de tag
        Args:
            data: tipo de tag a ser criado
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - tipo de tag criado
        """
        service = TipoTagService(
            TipoTagRepository(session, environment),
            environment
        )
        return await service.create(data)


    @router.put(path="/tipo_tags/{guid}", response_model=TipoTagOutput)
    @endpoint_exception_handler
    async def put_tag(self, guid, data: TipoTagInput,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para atualizar um tipo de tag
        Args:
            data: tipo de tag a ser atualizado
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - tipo de tag atualizado
        """
        service = TipoTagService(
            TipoTagRepository(session, environment),
            environment
        )
        return await service.update_by_guid(guid=guid, tipo_tag_input=data)

    @router.delete(path="/tipo_tags/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_tag(self, guid: str,
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para deletar um tipo de tag
        Args:
            guid: guid do projeto
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 204 (no content)
        """
        service = TipoTagService(
            TipoTagRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
