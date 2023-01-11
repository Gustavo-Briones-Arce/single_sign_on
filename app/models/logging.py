from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from app.config.database import Base


class Logging(Base):
    __tablename__ = 'loggings'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    user_name = Column(String(50))
    web_id = Column(String(50))
    web_name = Column(String(50))
    on_sign = Column(DateTime, default=datetime.now)
