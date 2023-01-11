from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.documentation.web import WEB_CREATE
from app.schemas.details import WebDetail
from app.schemas.web import Web, WebCreate, WebUpdate
from app.services.web import WebService


web_route = APIRouter(prefix='/web', tags=['Web'])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@web_route.get('/', response_model=list[Web])
async def get_all(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return WebService(session=session).get_all(skip=skip, limit=limit)


@web_route.post('/', name='New Website', description=WEB_CREATE, response_model=Web)
async def create_web(web: WebCreate, session: Session = Depends(get_db)):
    return WebService(session=session).new_web(web=web)


@web_route.put('/{id}', name='Update Website', description='Update a website', response_model=Web)
async def update_web(id: UUID4, web: WebUpdate, session: Session = Depends(get_db)):
    return WebService(session=session).update_web(id=str(id), web=web)


@web_route.delete('/{id}', name='Delete Website', description='Delete a website')
async def delete_web(id: UUID4, session: Session = Depends(get_db)):
    return WebService(session=session).delete_web(id=str(id))


@web_route.get('/{id}', name='Website detail', description='Get detail of the website by id', response_model=WebDetail)
async def detail_web(id: UUID4, session: Session = Depends(get_db)):
    return WebService(session=session).get_one(id=str(id))
