from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleMenu, RoleUpdate


class RoleService():

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.session.query(Role).offset(skip).limit(limit).all()

    def create_role(self, role: RoleCreate):
        if self.session.query(Role).filter(Role.name == role.name).one_or_none():
            raise HTTPException(status_code=400, detail='Role name exists')
        db_role = Role(**role.dict())
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return db_role

    def update_role(self, id: str, role: RoleUpdate):
        db_role = self.session.get(Role, id)
        if not db_role:
            raise HTTPException(status_code=404, detail='Role not found')
        if self.session.query(Role).filter(Role.name == role.name).one_or_none():
            raise HTTPException(status_code=400, detail='Role name exists')
        role_data = role.dict(exclude_unset=True)
        for key, value in role_data.items():
            setattr(db_role, key, value)
        setattr(db_role, 'on_updated', datetime.now())
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return db_role

    def set_menus(self, id: str, menus: RoleMenu):
        db_role = self.session.get(Role, id)
        if not db_role:
            raise HTTPException(status_code=404, detail='Role not found')
        for id in menus.menus:
            menu = self.session.get(Menu, str(id))
            if not menu:
                raise HTTPException(status_code=404, detail='Menu not found')
            db_role.menus.append(menu)
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return db_role
