from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class TipoDeTagInput(AuthenticatorModelInput):

    nome: str = Field(example='Função Projeto Exemplo')
    descricao: str = Field(example='Descrição da função')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TipoDeTagOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    nome: str = Field(example='Função Projeto Exemplo')
    descricao: str = Field(example='Descrição da função')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True