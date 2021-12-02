import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class RelacaoProjetoCursoModel(db.Base, AuthenticatorBase):
    """
    Modelo da relação projeto curso
    possui relações com projeto e curso
    """
    def __init__(self, **kwargs):
        super(RelacaoProjetoCursoModel, self).__init__(**kwargs)

    __tablename__ = "tb_rel_projeto_curso"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    id_cursos = Column(BigInteger, ForeignKey("tb_curso.id"))

    projeto = relationship("ProjetosModel", back_populates="rel_projeto_curso")
    curso = relationship("CursoModel", back_populates="rel_projeto_curso")
