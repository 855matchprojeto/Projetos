import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class InteresseModel(db.Base, AuthenticatorBase):
    """
    Modelo de Curso
    possui relações com relacao_projeto_interesse
    """
    def __init__(self, **kwargs):
        super(InteresseModel, self).__init__(**kwargs)

    __tablename__ = "tb_interesse"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    nome_referencia = Column(String(), unique=True, nullable=False)
    nome_exibicao = Column(String(), unique=True, nullable=False)
    descricao = Column(String())

    relacao_projeto_interesse = relationship(
        "RelacaoProjetoInteresseModel",
        back_populates="interesse"
    )
