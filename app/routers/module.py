from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.details import ModuleDetail
from app.schemas.module import Module, ModuleCreate, ModuleUpdate
from app.services.module import ModuleService


module_route = APIRouter(prefix='/module', tags=['Module'])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@module_route.get('/')
async def get_all(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return ModuleService(session=session).get_all(skip=skip, limit=limit)


@module_route.post('/', name='New Module', description='Create a new Module', response_model=Module)
async def create_module(module: ModuleCreate, session: Session = Depends(get_db)):
    return ModuleService(session=session).create_module(module=module)


@module_route.put('/{id}', name='Update Module', description='Update a Module', response_model=Module)
async def update_module(id: UUID4, module: ModuleUpdate, session: Session = Depends(get_db)):
    return ModuleService(session=session).update_module(id=str(id), module=module)


@module_route.delete('/{id}', name='Delete Module', description='Delete a Module')
async def delete_module(id: UUID4, session: Session = Depends(get_db)):
    return ModuleService(session=session).delete_module(id=str(id))


@module_route.get('/{id}', name='Module detail', description='Get detail of a module by id', response_model=ModuleDetail)
async def get_detail(id: UUID4, session: Session = Depends(get_db)):
    return ModuleService(session=session).get_detail(id=str(id))
