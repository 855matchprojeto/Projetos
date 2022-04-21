from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr


class RelacaoProjetoInteresseInput(AuthenticatorModelInput):
    id_projetos: int = Field(example='1')
    id_interesses: int = Field(example='1')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RelacaoProjetoInteresseOutput(AuthenticatorModelInput):
    id: int = Field(example='1')
    id_projetos: int = Field(example='1')
    id_interesses: int = Field(example='1')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
