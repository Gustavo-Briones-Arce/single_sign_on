from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.details import RoleDetail
from app.schemas.role import Role, RoleCreate, RoleMenu
from app.services.role import RoleService


role_route = APIRouter(prefix='/role', tags=['Role'])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@role_route.get('/')
async def get_all(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return RoleService(session=session).get_all(skip=skip, limit=limit)


@role_route.post('/', name='Create Role', description='Create a new Role', response_model=Role)
async def create_role(role: RoleCreate, session: Session = Depends(get_db)):
    return RoleService(session=session).create_role(role=role)


@role_route.post('/{id}', name='Set Menu', description='Set the menu(s) to Role', response_model=RoleDetail)
async def set_menu(id: UUID4, menus: RoleMenu, session: Session = Depends(get_db)):
    return RoleService(session=session).set_menus(id=str(id), menus=menus)
