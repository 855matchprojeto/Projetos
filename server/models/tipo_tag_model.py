import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class TipoDeTagModel(db.Base, AuthenticatorBase):
    """
    Modelo do tipo de tag
    """
    def __init__(self, **kwargs):
        super(TipoDeTagModel, self).__init__(**kwargs)

    __tablename__ = "tb_tipo_de_tag"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    nome = Column(String(), nullable=False)
    descricao = Column(String(), nullable=False)
