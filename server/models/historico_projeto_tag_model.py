import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class HistoricoProjetoTagModel(db.Base, AuthenticatorBase):

    def __init__(self, **kwargs):
        super(HistoricoProjetoTagModel, self).__init__(**kwargs)

    __tablename__ = "tb_historico_projeto_tag"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    id_tags = Column(BigInteger, ForeignKey("tb_tags.id"))
    data = Column(DateTime, default=datetime.now)
    mudanca = Column(String(), nullable=False)