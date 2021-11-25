import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class EntidadeExternaModel(db.Base, AuthenticatorBase):

    def __init__(self, **kwargs):
        super(EntidadeExternaModel, self).__init__(**kwargs)

    __tablename__ = "tb_entidade_externa"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    nome = Column(String(), nullable=False)