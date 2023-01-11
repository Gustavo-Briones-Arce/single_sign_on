from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.models.module import Module
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuService():

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.session.query(Menu).offset(skip).limit(limit).all()

    def create_menu(self, menu: MenuCreate):
        if self.session.query(Menu).filter(Menu.module_id == menu.module_id, Menu.name == menu.name).one_or_none():
            raise HTTPException(
                status_code=400, detail='Existing name for the same module')
        db_menu = Menu(**menu.dict())
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def update_menu(self, id: str, menu: MenuUpdate):
        db_menu = self.session.get(Menu, id)
        if not db_menu:
            raise HTTPException(status_code=404, detail='Menu not found')
        if menu.module_id:
            if not self.session.get(Module, menu.module_id):
                raise HTTPException(status_code=404, detail='Module not found')
            setattr(db_menu, 'module_id', menu.module_id)
        menu_data = menu.dict(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(db_menu, key, value)
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def delete_menu(self, id: str):
        db_menu = self.session.get(Menu, id)
        if not db_menu:
            raise HTTPException(status_code=404, detail='Menu not found')
        self.session.delete(db_menu)
        self.session.commit()
        return JSONResponse(content='Website deleted', status_code=200)
