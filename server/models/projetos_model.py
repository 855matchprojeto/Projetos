import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class ProjetosModel(db.Base, AuthenticatorBase):
    """
    Modelo de projeto
    possui relações com entidade, tag e usuario
    """
    def __init__(self, **kwargs):
        super(ProjetosModel, self).__init__(**kwargs)

    __tablename__ = "tb_projetos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    titulo = Column(String(), nullable=False)
    descricao = Column(String())

    rel_projeto_entidade = relationship(
        "RelacaoProjetoEntidadeModel",
        back_populates="projeto"
    )

    rel_projeto_tag = relationship(
        "RelacaoProjetoTagModel",
        back_populates="projeto"
    )

    rel_projeto_usuario = relationship(
        "RelacaoProjetoUsuarioModel",
        back_populates="projeto"
    )

    rel_projeto_curso = relationship(
        "RelacaoProjetoCursoModel",
        back_populates="projeto"
    )

    relacao_projeto_interesse = relationship(
        "RelacaoProjetoInteresseModel",
        back_populates="projeto"
    )

    rel_projeto_interesse = relationship(
        "InteresseUsuarioProjeto",
        back_populates="projeto",
        cascade="all,delete"
    )
