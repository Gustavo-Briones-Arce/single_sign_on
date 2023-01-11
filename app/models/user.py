from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from app.config.database import Base, get_new_uuid


userRoleLink = Table(
    'user_role_link',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('on_created', DateTime, default=datetime.now)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=get_new_uuid)
    first_name = Column(String(50))
    last_name = Column(String(50))
    rut = Column(String(10), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(120))
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    activate_token = Column(String, default=get_new_uuid)
    reset_pass_token = Column(String)
    on_created = Column(DateTime, default=datetime.now)
    on_updated = Column(DateTime, default=datetime.now)
    roles = relationship(
        'Role', secondary=userRoleLink, back_populates='users')

    def payload(self) -> dict:
        return {'first_name': self.first_name, 'last_name': self.last_name, 'rut': self.rut, 'email': self.email}

    def get_menus(self):
        menus = []
        if self.roles:
            for roles in self.roles:
                menus.extend(roles.menus)
        return menus
