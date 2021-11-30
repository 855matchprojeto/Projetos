import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class RelacaoProjetoEntidadeModel(db.Base, AuthenticatorBase):
    """
    Modelo da relação projeto entidade
    possui relações com projeto e entidade
    """
    def __init__(self, **kwargs):
        super(RelacaoProjetoEntidadeModel, self).__init__(**kwargs)

    __tablename__ = "tb_rel_projeto_entidade"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    id_entidade = Column(BigInteger, ForeignKey("tb_entidade_externa.id"))

    projeto = relationship("ProjetosModel", back_populates="rel_projeto_entidade")
    entidade_externa = relationship("EntidadeExternaModel", back_populates="rel_projeto_entidade")
