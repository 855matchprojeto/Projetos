from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class RelacaoProjetoTagInput(AuthenticatorModelInput):

    id_projetos: int = Field(example="1")
    id_tags: int = Field(example="1")

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RelacaoProjetoTagOutput(AuthenticatorModelOutput):

    id: int = Field(example="1")
    id_projetos: int = Field(example="1")
    id_tags: int = Field(example="1")

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True