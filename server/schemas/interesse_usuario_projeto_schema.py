from server.schemas import AuthenticatorModelInput, AuthenticatorModelOutput
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID as GUID


class InteresseUsuarioProjetoOutput(AuthenticatorModelOutput):
    """
    Schema de output do interesse usuário projeto

    retorna também id, guid, created_at e updated_at criados
    """
    id: int = Field(example=1)
    guid: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')

    guid_usuario: GUID = Field(example='78628c23-aae3-4d58-84a9-0c8d7ea63672')
    id_projeto: int = Field(example=1)

    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

