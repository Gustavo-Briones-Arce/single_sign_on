from datetime import datetime

from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.config.database import Base, get_new_uuid
from app.models.role import roleMenuLink


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String(36), primary_key=True, default=get_new_uuid)
    name = Column(String(50))
    is_public = Column(Boolean, default=False)
    module_id = Column(String, ForeignKey('modules.id'))
    on_created = Column(DateTime, default=datetime.now)
    on_updated = Column(DateTime, default=datetime.now)

    module = relationship('Module', back_populates='menus')
    roles = relationship('Role', secondary=roleMenuLink,
                         back_populates='menus')
