from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class PermissaoInput(AuthenticatorModelInput):

    nome: str = Field(example='Lucas Andre')
    descricao: str = Field(example='Quero o roberci fora do meu grupo')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PermissaoOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    nome: str = Field(example='Lucas Andre')
    descricao: str = Field(example='Quero o roberci fora do meu grupo')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True