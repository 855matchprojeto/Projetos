from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from uuid import UUID as GUID
from typing import List, Optional


class CursoInput(AuthenticatorModelInput):
    """
    Schema de input do curso
    """
    nome_referencia: str = Field(example='Nome referência Exemplo')
    nome_exibicao: str = Field(example='Nome de exibição Exemplo')
    descricao: str = Field(example='Descrição Exemplo')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CursoOutput(AuthenticatorModelOutput):
    """
    Schema de output do curso

    retorna também id e guid criados
    """
    id: int = Field(example="1")
    nome_referencia: str = Field(example='Nome referência Exemplo')
    nome_exibicao: str = Field(example='Nome de exibição Exemplo')
    descricao: str = Field(example='Descrição Exemplo')
    guid: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
