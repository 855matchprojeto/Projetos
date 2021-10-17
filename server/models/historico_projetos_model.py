import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime




class HistoricoProjetosModel(db.Base, AuthenticatorBase):

    def __init__(self, **kwargs):
        super(HistoricoProjetosModel, self).__init__(**kwargs)

    __tablename__ = "tb_historico_projetos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    titulo = Column(String(), nullable=False, unique=True)
    descricao = Column(String(), unique=True)
    data = Column(DateTime, default=datetime.now)