from fastapi import APIRouter, Depends, Security, status, Response
from fastapi_utils.cbv import cbv
from typing import Optional
from typing import List
from server.services.curso_service import CursoService
from server.schemas.curso_schema import CursoInput, CursoOutput
from server.dependencies.get_current_user import get_current_user
from server.schemas import usuario_schema
from server.controllers import endpoint_exception_handler
from server.configuration.db import AsyncSession
from server.dependencies.session import get_session
from server.configuration.environment import Environment
from server.dependencies.get_environment_cached import get_environment_cached
from server.repository.curso_repository import CursoRepository


router = APIRouter()

curso_router = dict(
    router=router,
    tags=["Curso"],
)


@cbv(router)
class CursoController:
    @router.get("/curso", response_model=List[CursoOutput])
    @endpoint_exception_handler
    async def get_curso(self, id: Optional[int] = None, guid: Optional[str] = None,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])
                           ):
        """
        Endpoint para pegar todas as curso
        Args:
            id: (optional) id do curso
            guid: (optional) guid do curso
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - lista com cursos
        """
        service = CursoService(
            CursoRepository(session, environment),
            environment
        )
        return await service.get(id=id, guid=guid)

    @router.post(path="/curso", response_model=CursoOutput)
    @endpoint_exception_handler
    async def post_curso(self, data: CursoInput,
                            session: AsyncSession = Depends(get_session),
                            environment: Environment = Depends(get_environment_cached),
                            current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para criar um novo curso
        Args:
            data: curso a ser criado
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - curso criado
        """
        service = CursoService(
            CursoRepository(session, environment),
            environment
        )
        return await service.create(data)


    @router.put(path="/curso/{guid}", response_model=CursoOutput)
    @endpoint_exception_handler
    async def put_curso(self, guid, data: CursoInput,
                           session: AsyncSession = Depends(get_session),
                           environment: Environment = Depends(get_environment_cached),
                           current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para atualizar um curso pelo guid
        Args:
            guid: guid do curso
            data: curso a ser modificada
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 200 (ok) - curso atualizado
        """
        service = CursoService(
            CursoRepository(session, environment),
            environment
        )
        return await service.update_by_guid(guid=guid, curso_input=data)

    @router.delete(path="/curso/{guid}", status_code=status.HTTP_204_NO_CONTENT,)
    @endpoint_exception_handler
    async def delete_curso(self, guid: str,
                              session: AsyncSession = Depends(get_session),
                              environment: Environment = Depends(get_environment_cached),
                              current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[])):
        """
        Endpoint para deletar um curso
        Args:
            guid: guid do curso
            session: seção para funcionamento da api
            environment: configurações de ambiente
            current_user: usuário fazendo a requisição

        Returns:
            código 204 (no content)
        """
        service = CursoService(
            CursoRepository(session, environment),
            environment
        )
        await service.delete(guid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
