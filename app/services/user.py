from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.shared.password import generate_password


class UserService():

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.session.query(User).offset(skip).limit(limit).all()

    def get_one_by_id(self, id: str):
        return self.session.get(User, id)

    def get_one_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).one_or_none()

    def get_one_by_rut(self, rut: str):
        return self.session.query(User).filter(User.rut == rut).one_or_none()

    def create_user(self, user: UserCreate):
        if self.session.query(User).filter(User.email == user.email).one_or_none():
            raise HTTPException(status_code=400, detail='Email exists')
        if self.session.query(User).filter(User.rut == user.rut).one_or_none():
            raise HTTPException(status_code=400, detail='Rut exists')
        user.password = generate_password(user.password)
        db_user = User(**user.dict())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def update_user(self, id: str, user: UserUpdate):
        db_user = self.session.get(User, id)
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')
        if user.password:
            user.password = generate_password(user.password)
        data_user = user.dict(exclude_unset=True)
        for key, value in data_user.items():
            setattr(db_user, key, value)
        setattr(db_user, 'on_updated', datetime.now())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete_user(self, id: str):
        db_user = self.session.get(User, id)
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')
        self.session.delete(db_user)
        self.session.commit()
        return JSONResponse(content='User deleted', status_code=200)
