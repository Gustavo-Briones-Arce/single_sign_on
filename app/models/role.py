from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from app.config.database import Base, get_new_uuid
from app.models.user import userRoleLink


roleMenuLink = Table(
    'role_menu_link',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('menu_id', ForeignKey('menus.id'), primary_key=True),
    Column('on_created', DateTime, default=datetime.now)
)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(String(36), primary_key=True, default=get_new_uuid)
    name = Column(String(50))
    on_created = Column(DateTime, default=datetime.now)
    on_updated = Column(DateTime, default=datetime.now)

    users = relationship(
        'User', secondary=userRoleLink, back_populates='roles')
    menus = relationship(
        'Menu', secondary=roleMenuLink,  back_populates='roles')
        
