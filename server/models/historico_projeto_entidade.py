import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class HistoricoProjetoEntidadeModel(db.Base, AuthenticatorBase):
    """
    Modelo do histórico projeto entidade
    possui relações com projeto e entidade
    """
    def __init__(self, **kwargs):
        super(HistoricoProjetoEntidadeModel, self).__init__(**kwargs)

    __tablename__ = "tb_historico_projeto_entidade"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_historico = Column(BigInteger, ForeignKey("tb_historico_projeto.id"))
    id_entidade = Column(BigInteger, ForeignKey("tb_entidade_externa.id"))
    data = Column(DateTime, default=datetime.now)
    mudanca = Column(String(), nullable=False)

    historico_projeto = relationship("HistoricoProjetoModel", back_populates="historico_projeto_entidade")
    entidade_externa = relationship("EntidadeExternaModel", back_populates="historico_projeto_entidade")
