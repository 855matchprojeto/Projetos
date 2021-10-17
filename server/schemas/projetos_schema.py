from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class ProjetosInput(AuthenticatorModelInput):

    titulo: str = Field(example='Projeto Exemplo')
    guid: str = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    descricao: str = Field(example='Isso é um projeto')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProjetosOutput(AuthenticatorModelOutput):
    id: int = Field(example="1")
    titulo: str = Field(example='Projeto Exemplo')
    guid: str = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    descricao: str = Field(example='Isso é um projeto')
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True