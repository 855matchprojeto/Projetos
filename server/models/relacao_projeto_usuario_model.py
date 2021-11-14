import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID



class RelacaoProjetoUsuarioModel(db.Base, AuthenticatorBase):

    def __init__(self, **kwargs):
        super(RelacaoProjetoUsuarioModel, self).__init__(**kwargs)

    __tablename__ = "tb_rel_projeto_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projetos = Column(BigInteger, ForeignKey("tb_projetos.id"))
    id_funcao = Column(BigInteger, ForeignKey("tb_funcao_projeto.id"))
    guid_user = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
