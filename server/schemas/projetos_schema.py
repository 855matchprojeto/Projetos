from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput, ProjetosModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID as GUID
from server.schemas.arquivo_schema import ArquivoInput, ArquivoOutput
from server.schemas.entidade_externa_schema import EntidadeExternaOutput
from server.schemas.tag_schema import TagOutput
from server.schemas.interesse_schema import InteresseOutput
from server.schemas.curso_schema import CursoOutput
from server.schemas.interesse_usuario_projeto_schema import InteresseUsuarioProjetoOutput
from fastapi import Query


InterestQuery = Query(
    None,
    title="Query string para filtrar projetos a partir dos IDS dos interesses vinculados ao projeto",
    description="Query string para filtrar projetos a partir dos IDS dos interesses vinculados ao projeto"
)

CourseQuery = Query(
    None,
    title="Query string para filtrar projetos a partir dos IDS dos cursos vinculados ao projeto",
    description="Query string para filtrar projetos a partir dos IDS dos cursos vinculados ao projeto",
)

class ProjetosInputUpdate(AuthenticatorModelInput):
    """
    Schema de input do projeto para update
    """
    titulo: Optional[str] = Field(example='Projeto Exemplo')
    descricao: Optional[str] = Field(example='Isso é um projeto')
    url_imagem: Optional[str] = Field(example='https://teste.com.br')

    id_imagem_projeto: Optional[int] = Field(example='2')
    imagem_projeto: Optional[ArquivoInput]

    def convert_to_dict(self):
        return self.dict(exclude_unset=True)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

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
    url_imagem: Optional[str] = Field(example='https://teste.com.br')

    id_imagem_projeto: Optional[int] = Field(example='2')
    imagem_projeto: Optional[ArquivoInput]

    def convert_to_dict(self):
        return self.dict(exclude_unset=True)

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
    url_imagem: Optional[str] = Field(example='https://teste.com.br')
    id_imagem_projeto: Optional[int] = Field(example='2')
    imagem_projeto: Optional[ArquivoOutput]
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
    url_imagem: Optional[str] = Field(example='https://teste.com.br')
    id_imagem_projeto: Optional[int] = Field(example='2')
    imagem_projeto: Optional[ArquivoOutput]
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProjetoAndOwnInteresseUsuarioProjetoOutput(SimpleProjetosOutput):

    interesse_usuario_projeto: InteresseUsuarioProjetoOutput

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PaginatedProjetoOutput(ProjetosModelOutput):

    items: List[ProjetosOutput]
    count: Optional[int] = Field(example='10')
    previous_cursor: Optional[str] = Field(example='previous_cursor_token')
    next_cursor: Optional[str] = Field(example='next_cursor_token')
    previous_url: Optional[str] = Field(example='http://localhost/projetos-pag/?page_size=10&cursor=previous_cursor_token')
    next_url: Optional[str] = Field(example='http://localhost/projetos-pag/?page_size=10&cursor=next_cursor_token')

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True




