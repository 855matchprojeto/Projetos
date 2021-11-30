import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class EntidadeExternaModel(db.Base, AuthenticatorBase):
    """
    Modelo da entidade externa
    possui relações com projeto e histórico
    """
    def __init__(self, **kwargs):
        super(EntidadeExternaModel, self).__init__(**kwargs)

    __tablename__ = "tb_entidade_externa"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    nome = Column(String(), nullable=False)

    rel_projeto_entidade = relationship(
        "RelacaoProjetoEntidadeModel",
        back_populates="entidade_externa"
    )

    historico_projeto_entidade = relationship(
        "HistoricoProjetoEntidadeModel",
        back_populates="entidade_externa"
    )
