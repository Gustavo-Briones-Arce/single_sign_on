from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import UserService


user_route = APIRouter(prefix='/user', tags=['User'])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_route.get('/', name='All Users', description='Get all User', response_model=list[User])
def get_all(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return UserService(session=session).get_all(skip=skip, limit=limit)


@user_route.post('/', name='Create User', description='Create a new user', response_model=User)
async def create_user(user: UserCreate, session: Session = Depends(get_db)):
    return UserService(session=session).create_user(user=user)


@user_route.put('/{id}', name='Update User', description='Update a user', response_model=User)
async def update_user(id: UUID4, user: UserUpdate, session: Session = Depends(get_db)):
    return UserService(session=session).update_user(id=str(id), user=user)


@user_route.delete('/{id}', name='Delete User', description='Developing...', response_model=User)
async def delete_user(id: UUID4, session: Session = Depends(get_db)):
    return UserService(session=session).delete_user(id=str(id))


@user_route.post('/{id}', name='Set Role', description='Set Roles to User. Developing...')
async def set_roles():
    pass
