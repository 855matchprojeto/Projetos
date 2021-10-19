from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class HistoricoProjetoEntidadeInput(AuthenticatorModelInput):

    id_projetos: int = Field(example="1")
    id_entidade: int = Field(example="1")
    data: datetime = Field(None)
    mudanca: str = Field(example='Quero o roberci fora do meu grupo')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class HistoricoProjetoEntidadeOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    id_projetos: int = Field(example="1")
    id_entidade: int = Field(example="1")
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)
    mudanca: str = Field(example='Quero o roberci fora do meu grupo')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True