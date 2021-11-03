from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from uuid import UUID as GUID
from typing import List, Optional


class TipoTagInput(AuthenticatorModelInput):
    nome: str = Field(example='Tipo Tag Exemplo')
    descricao: str = Field(example='Descrição de um tipo de tag')
    guid: Optional[GUID] = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TipoTagOutput(AuthenticatorModelOutput):
    id: int = Field(example="1")
    nome: str = Field(example='Tipo Tag Exemplo')
    descricao: str = Field(example='Descrição de um tipo de tag')
    guid: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
