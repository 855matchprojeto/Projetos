from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from uuid import UUID as GUID
from typing import List, Optional


class TagInput(AuthenticatorModelInput):
    nome: str = Field(example='Tag Exemplo')
    nome_de_referencia: str = Field(example='Nome de referência Tag Exemplo')
    descricao: str = Field(example='Descrição da tag')
    id_tipo_de_tag: int = Field(example="1")
    guid: Optional[GUID] = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TagOutput(AuthenticatorModelOutput):
    id: int = Field(example="1")
    nome: str = Field(example='Tag Exemplo')
    nome_de_referencia: str = Field(example='Nome de referência Tag Exemplo')
    descricao: str = Field(example='Descrição da tag')
    id_tipo_de_tag: int = Field(example="1")
    guid: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
