from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from uuid import UUID as GUID
from typing import List, Optional


class FuncaoProjetosInput(AuthenticatorModelInput):
    """
    Schema de input da função
    """
    nome: str = Field(example='Função Projeto Exemplo')
    descricao: str = Field(example='Descrição da função')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FuncaoProjetosOutput(AuthenticatorModelOutput):
    """
    Schema de output da função

    retorna também id, guid, created_at e updated_at criados
    """
    id: int = Field(example="1")
    nome: str = Field(example='Função Projeto Exemplo')
    guid: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    descricao: str = Field(example='Descrição da função')
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True