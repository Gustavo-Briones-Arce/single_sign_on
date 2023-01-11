from fastapi import APIRouter, Depends, Request
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.middleware.jwt_bearer import JWTBearer
from app.schemas.auth import Access, Logging, LoggingRut, Token
from app.services.auth import AuthService
from app.shared.jwt import validation_token


auth_route = APIRouter(prefix='/auth', tags=['Auth'])

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_route.post('/logging/{web_id}', name='Logging with email', description='Sign-On! In addition to the credentials it is necessary to send web-id', response_model=Token)
async def logging(web_id: UUID4, logging: Logging, session: Session = Depends(get_db)):
    return AuthService(session=session).sign_on_by_email(web_id=str(web_id), logging=logging)


@auth_route.post('/logging/rut/{web_id}', name='Logging with rut', description='Sign-On! In addition to the credentials it is necessary to send web-id', response_model=Token)
async def logging(web_id: UUID4, logging: LoggingRut, session: Session = Depends(get_db)):
    return AuthService(session=session).sign_on_by_rut(web_id=str(web_id), logging=logging)


@auth_route.get('/access/{web_id}', name='Access to Website', description='Get access list. Modules with the menus that the user has access to', dependencies=[Depends(JWTBearer())])
async def access(web_id: UUID4, req: Request, session: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    data_user = validation_token(token=token.replace('Bearer ', ''))
    return AuthService(session=session).get_access_by_id_web(email=data_user['email'], web_id=str(web_id))
