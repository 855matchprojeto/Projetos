import uuid
from uuid import UUID as GUID
from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.dialects.postgresql import UUID


class InteresseUsuarioProjeto(db.Base, AuthenticatorBase):

    """
        Tabela para armazenar projetos que
        o usuário marcou como "Interesse"
    """

    __table_args__ = (
        UniqueConstraint('guid_usuario', 'id_projeto'),
    )

    def __init__(self, **kwargs):
        super(InteresseUsuarioProjeto, self).__init__(**kwargs)

    __tablename__ = "tb_interesse_usuario_projeto"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)

    guid_usuario = Column(UUID(as_uuid=True), nullable=False, unique=False, default=uuid.uuid4)
    id_projeto = Column(BigInteger, ForeignKey("tb_projetos.id"))

