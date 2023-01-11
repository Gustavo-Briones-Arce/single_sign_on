from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.menu import Menu, MenuCreate, MenuUpdate
from app.services.menu import MenuService


menu_route = APIRouter(prefix='/menu', tags=['Menu'])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@menu_route.get('/', name='All Menu', description='Get all menu', response_model=list[Menu])
def get_all(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return MenuService(session=session).get_all(skip=skip, limit=limit)


@menu_route.post('/', name='New Menu', description='Create a new menu', response_model=Menu)
async def create_menu(menu: MenuCreate, session: Session = Depends(get_db)):
    return MenuService(session=session).create_menu(menu=menu)


@menu_route.put('/{id}', name='Update Menu', description='Update a menu', response_model=Menu)
async def update_menu(id: UUID4, menu: MenuUpdate, session: Session = Depends(get_db)):
    return MenuService(session=session).update_menu(id=str(id), menu=menu)


@menu_route.delete('/{id}', name='Delete Menu', description='Delete a Menu')
async def delete_menu(id: UUID4, session: Session = Depends(get_db)):
    return MenuService(session=session).delete_menu(id=str(id))
