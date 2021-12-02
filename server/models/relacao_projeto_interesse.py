import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class RelacaoProjetoInteresseModel(db.Base, AuthenticatorBase):
    """
    Modelo da relação projeto interesse
    possui relações com projeto e interesse
    """
    def __init__(self, **kwargs):
        super(RelacaoProjetoInteresseModel, self).__init__(**kwargs)

    __tablename__ = "tb_rel_projeto_interesse"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    id_interesses = Column(BigInteger, ForeignKey("tb_interesse.id"))

    projeto = relationship("ProjetosModel", back_populates="relacao_projeto_interesse")
    interesse = relationship("InteresseModel", back_populates="relacao_projeto_interesse")
