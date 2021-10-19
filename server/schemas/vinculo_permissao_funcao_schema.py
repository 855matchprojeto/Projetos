from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class VinculoPermissaoFuncaoInput(AuthenticatorModelInput):

    id_permissao: int = Field(example="1")
    id_funcao: int = Field(example="1")

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VinculoPermissaoFuncaoOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    nome: str = Field(example='Função Projeto Exemplo')
    descricao: str = Field(example='Descrição da função')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True