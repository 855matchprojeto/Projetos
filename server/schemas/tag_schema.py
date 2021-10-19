from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class TagInput(AuthenticatorModelInput):

    nome: str = Field(example='Função Projeto Exemplo')
    nome_de_referencia: str = Field(example='Função Projeto Exemplo')
    id_tipo_de_tag: int = Field(example="1")
    descricao: str = Field(example='Descrição da função')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TagOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    nome: str = Field(example='Função Projeto Exemplo')
    nome_de_referencia: str = Field(example='Função Projeto Exemplo')
    id_tipo_de_tag: int = Field(example="1")
    descricao: str = Field(example='Descrição da função')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True