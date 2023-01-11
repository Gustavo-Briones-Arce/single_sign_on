from pydantic import BaseModel, EmailStr


class LoggingBase(BaseModel):
    password: str


class Logging(LoggingBase):
    email: EmailStr


class LoggingRut(LoggingBase):
    rut: str


class Token(BaseModel):
    accessToken: str
    refreshToken: str


class Access(BaseModel):
    module: str
    menus: list[str]
