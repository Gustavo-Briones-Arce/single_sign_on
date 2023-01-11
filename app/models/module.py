from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.config.database import Base, get_new_uuid


class Module(Base):
    __tablename__ = 'modules'

    id = Column(String(36), primary_key=True, default=get_new_uuid)
    name = Column(String(50))
    description = Column(String(100), nullable=True)
    web_id = Column(String, ForeignKey('webs.id'))
    on_created = Column(DateTime, default=datetime.now)
    on_updated = Column(DateTime, default=datetime.now)

    web = relationship('Web', back_populates='modules')
    menus = relationship('Menu', back_populates='module')
