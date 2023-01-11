from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ModuleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    web_id: Optional[str]


class Module(ModuleBase):
    id: str
    on_created: datetime
    on_updated: Optional[datetime]

    class Config:
        orm_mode = True


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(ModuleBase):
    pass
