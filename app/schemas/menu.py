from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    name: Optional[str]
    is_public: Optional[bool]
    module_id: Optional[str]


class Menu(MenuBase):
    id: str
    on_created: datetime
    on_updated: Optional[datetime]

    class Config:
        orm_mode = True


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass
