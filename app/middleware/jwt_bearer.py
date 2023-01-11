from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.user import User
from app.shared.jwt import validation_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, session: Session = Depends(get_db)):
        jwt = await super().__call__(request)
        data = validation_token(jwt.credentials)
        if not session.query(User).filter(User.email == data['email']).one_or_none():
            raise HTTPException(status_code=403, detail='Invalid jwt')
