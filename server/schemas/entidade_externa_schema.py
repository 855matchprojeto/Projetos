from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from uuid import UUID as GUID
from typing import List, Optional


class EntidadeExternaInput(AuthenticatorModelInput):
    """
    Schema de input da entidade externa
    """
    nome: str = Field(example='Tipo Tag Exemplo')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EntidadeExternaOutput(AuthenticatorModelOutput):
    """
    Schema de output da entidade externa

    retorna também id e guid criados
    """
    id: int = Field(example="1")
    nome: str = Field(example='Tipo Entidade Externa Exemplo')
    guid: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
