from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr


class RelacaoProjetoEntidadeInput(AuthenticatorModelInput):
    id_projetos: int = Field(example='1')
    id_entidade: int = Field(example='2')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RelacaoProjetoEntidadeOutput(AuthenticatorModelInput):
    id: int = Field(example='1')
    id_projetos: int = Field(example='1')
    id_entidade: int = Field(example='1')

    def convert_to_dict(self):
        return self.dict()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
