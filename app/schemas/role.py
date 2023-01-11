from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class RoleBase(BaseModel):
    name: Optional[str]


class Role(RoleBase):
    id: str
    on_created: datetime
    on_updated: Optional[datetime]

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleMenu(BaseModel):
    menus: list[UUID4]
