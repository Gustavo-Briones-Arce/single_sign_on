from pydantic import BaseSettings


class Setting(BaseSettings):
    # Connection database
    SQL_HOST: str
    SQL_PORT: str
    SQL_USER: str
    SQL_PASSWORD: str
    SQL_DB: str

    # JWT
    SECRET_KEY: str
    REFRESH_KEY: str
    EXP_TOKEN: int

    # Default Data
    DEFAULT_NAME: str
    DEFAULT_LAST_NAME: str
    DEFAULT_EMAIL: str
    DEFAULT_PASSWORD: str
    DEFAULT_RUT: str
    DEFAULT_URL: str
    # PASSWORD
    KEY_PASSWORD: str

    class Config:
        env_file = '.env'


setting = Setting()
