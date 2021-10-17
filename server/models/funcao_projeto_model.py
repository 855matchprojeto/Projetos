import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class FuncaoProjeto(db.Base, AuthenticatorBase):

    def __init__(self, **kwargs):
        super(FuncaoProjeto, self).__init__(**kwargs)

    __tablename__ = "tb_funcao_projeto"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    nome = Column(String(), nullable=False, unique=True)
    descricao = Column(String(), unique=True)

