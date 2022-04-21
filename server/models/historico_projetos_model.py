import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class HistoricoProjetoModel(db.Base, AuthenticatorBase):
    """
    Modelo do histórico do projeto
    possui relações com entidade, tag e usuario
    """
    def __init__(self, **kwargs):
        super(HistoricoProjetoModel, self).__init__(**kwargs)

    __tablename__ = "tb_historico_projeto"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    titulo = Column(String(), nullable=False)
    descricao = Column(String())
    url_imagem = Column(String())
    data = Column(DateTime, default=datetime.now)

    historico_projeto_entidade = relationship(
        "HistoricoProjetoEntidadeModel",
        back_populates="historico_projeto"
    )

    historico_projeto_tag = relationship(
        "HistoricoProjetoTagModel",
        back_populates="historico_projeto"
    )

    # historico_projeto_usuario = relationship(
    #     "HistoricoProjetoUsuarioModel",
    #     back_populates="historico_projeto"
    # )
