from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class HistoricoProjetoUsuarioInput(AuthenticatorModelInput):

    id_projetos: int = Field(example="1")
    guid: str = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    data: datetime = Field(None)
    mudanca: str = Field(example='Quero o roberci fora do meu grupo')
    funcao: str = Field(example='Nenhuma')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class HistoricoProjetoUsuarioOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    id_projetos: int = Field(example="1")
    guid: str = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    data: datetime = Field(None)
    mudanca: str = Field(example='Quero o roberci fora do meu grupo')
    funcao: str = Field(example='Nenhuma')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True