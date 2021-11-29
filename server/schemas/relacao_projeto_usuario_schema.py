from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class RelacaoProjetoUsuarioInput(AuthenticatorModelInput):

    id_projetos: int = Field(example="1")
    id_funcao: int = Field(example="1")
    guid_user: str = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RelacaoProjetoUsuarioOutput(AuthenticatorModelOutput):
    id: int = Field(example="1")
    id_projetos: int = Field(example="1")
    id_funcao: int = Field(example="1")
    guid_user: str = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True