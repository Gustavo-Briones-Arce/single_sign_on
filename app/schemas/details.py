
from app.schemas.menu import Menu
from app.schemas.module import Module
from app.schemas.role import Role
from app.schemas.web import Web


class WebDetail(Web):
    modules: list[Module]


class ModuleDetail(Module):
    menus: list[Menu]


class MenuDetail(Menu):
    roles: list[Role]


class RoleDetail(Role):
    menus: list[Menu]
