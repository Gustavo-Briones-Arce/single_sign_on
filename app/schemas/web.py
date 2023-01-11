from datetime import datetime
from typing import Optional
from pydantic import HttpUrl, BaseModel


class WebBase(BaseModel):
    name: Optional[str]
    url: Optional[HttpUrl]
    is_frontend: Optional[bool]


class Web(WebBase):
    id: str
    on_created: datetime
    on_updated: Optional[datetime]

    class Config:
        orm_mode = True


class WebCreate(WebBase):
    pass


class WebUpdate(WebBase):
    pass
