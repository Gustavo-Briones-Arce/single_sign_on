from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.models.user import User
from app.models.web import Web
from app.schemas.auth import Access, Logging, LoggingRut, Token
from app.shared.jwt import create_token
from app.shared.password import validate_password


class AuthService():

    def __init__(self, session: Session) -> None:
        self.session = session

    def sign_on_by_email(self, web_id: str, logging: Logging):
        web = self.session.get(Web, web_id)
        if not web:
            raise HTTPException(status_code=403)

        user = self.session.query(User).filter(
            User.email == logging.email).one_or_none()
        if not user:
            raise HTTPException(status_code=403)
        return self.sign_on(web=web, user=user, password=logging.password)

    def sign_on_by_rut(self, web_id: str, logging: LoggingRut):
        web = self.session.get(Web, web_id)
        if not web:
            raise HTTPException(status_code=403)

        user = self.session.query(User).filter(
            User.rut == logging.rut).one_or_none()
        if not user:
            raise HTTPException(status_code=403)
        self.sign_on(web=web, user=user, password=logging.password)

    def sign_on(self, web: Web, user: User, password: str):
        if not user.is_admin:
            if not web.contains_modules_with_public_menus():
                if len(user.get_menus()) == 0:
                    raise HTTPException(status_code=403)
                if not self.menus_user_in_menus_web(menus_user=user.get_menus(), menus_web=web.get_menus()):
                    raise HTTPException(status_code=403)

        if not validate_password(password=password, hash_password=user.password):
            raise HTTPException(status_code=403)
        return Token(accessToken=create_token(data=user.payload(), type='access'), refreshToken=create_token(data=user.payload()))

    def menus_user_in_menus_web(self, menus_user: list[Menu], menus_web: list[Menu]) -> bool:
        for menu in menus_user:
            if menu in menus_web:
                return True
        return False

    def get_access_by_id_web(self, email: str, web_id: str):
        db_user = self.session.query(User).filter(
            User.email == email).one_or_none()
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')
        db_web = self.session.get(Web, web_id)
        if not db_web:
            raise HTTPException(status_code=404, detail='Website not found')
        list_access = []
        if db_user.is_admin:
            for module in db_web.modules:
                if not module.menus:
                    continue
                menus: list[str] = []
                for menu in module.menus:
                    menus.append(menu.name)
                access = Access(module=module.name, menus=menus)
                list_access.append(access)
            return list_access
        else:
            for module in db_web.modules:
                if not module.menus:
                    continue
                menus: list[str] = []
                for menu in module.menus:
                    if menu in db_user.get_menu():
                        menus.append(menu.name)
                if len(menus) > 0:
                    access = Access(module=module.name, menus=menus)
                    list_access.append(access)
            return list_access
