import uuid
from uuid import UUID as GUID

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from server.models import AuthenticatorBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class TagModel(db.Base, AuthenticatorBase):

    def __init__(self, **kwargs):
        super(TagModel, self).__init__(**kwargs)

    __tablename__ = "tb_tag"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(), nullable=False)
    nome_de_referencia = Column(String(), nullable=False)
    id_tipo_de_tag = Column(BigInteger, ForeignKey("tb_tipos_de_tags.id"))
    descricao = Column(String(), nullable=False)
