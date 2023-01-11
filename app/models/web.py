from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.config.database import Base, get_new_uuid


class Web(Base):
    __tablename__ = 'webs'

    id = Column(String(36), primary_key=True, default=get_new_uuid)
    name = Column(String(length=50))
    url = Column(String(200))
    is_frontend = Column(Boolean, default=False)
    on_created = Column(DateTime, default=datetime.now)
    on_updated = Column(DateTime, default=None)
    modules = relationship('Module', back_populates='web')

    def contains_modules_with_public_menus(self) -> bool:
        for module in self.modules:
            for menu in module.menus:
                if menu.is_public:
                    return True
        return False

    def get_menus(self):
        menus = []
        for module in self.modules:
            menus.extend(module.menus)
        return menus
