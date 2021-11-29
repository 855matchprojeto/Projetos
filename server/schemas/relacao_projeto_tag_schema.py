from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID as GUID

from server.schemas.entidade_externa_schema import EntidadeExternaOutput
from server.schemas.tag_schema import TagOutput


class RelacaoProjetoTagInput(AuthenticatorModelInput):
    id_projeto: int = Field(example='1')
    id_tags: int = Field(example='2')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RelacaoProjetoTagOutput(AuthenticatorModelInput):
    id: int = Field(example='1')
    id_projeto: int = Field(example='1')
    id_tag: int = Field(example='1')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
