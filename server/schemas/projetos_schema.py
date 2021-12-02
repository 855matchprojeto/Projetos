from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID as GUID

from server.schemas.entidade_externa_schema import EntidadeExternaOutput
from server.schemas.tag_schema import TagOutput
from server.schemas.interesse_schema import InteresseOutput
from server.schemas.curso_schema import CursoOutput


class ProjetosInput(AuthenticatorModelInput):
    """
    Schema de input do projeto
    """
    titulo: str = Field(example='Projeto Exemplo')
    descricao: str = Field(example='Isso é um projeto')
    entidades: Optional[List[int]] = Field(example=[])
    tags: Optional[List[int]] = Field(example=[])
    cursos: Optional[List[int]] = Field(example=[])
    interesses: Optional[List[int]] = Field(example=[])



    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProjetosOutput(AuthenticatorModelOutput):
    """
    Schema de output do projeto

    retorna também id, guid, entidades, tags, created_at e updated_at criados
    """
    id: int = Field(example="1")
    titulo: str = Field(example='Projeto Exemplo')
    guid: Optional[GUID] = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    descricao: str = Field(example='Isso é um projeto')
    entidades: Optional[List[EntidadeExternaOutput]] = Field(example=[])
    tags: Optional[List[TagOutput]] = Field(example=[])
    cursos: Optional[List[CursoOutput]] = Field(example=[])
    interesses: Optional[List[InteresseOutput]] = Field(example=[])
    # usuarios: List[UsuarioOutput] = Field(example=[])
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SimpleProjetosOutput(AuthenticatorModelOutput):
    id: int = Field(example="1")
    titulo: str = Field(example='Projeto Exemplo')
    guid: Optional[GUID] = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    descricao: str = Field(example='Isso é um projeto')
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

