from datetime import datetime, timedelta
from jwt import decode, encode

from app.config.setting import setting
from app.models.user import User


def create_token(data: dict, type: str = 'refresh') -> str:
    data['iat'] = datetime.utcnow()
    if type == 'access':
        data['exp'] = datetime.utcnow() + timedelta(hours=1)
    else:
        data['exp'] = datetime.utcnow() + timedelta(days=1)
    return encode(payload=data, key=setting.SECRET_KEY)


def validation_token(token: str) -> dict:
    return decode(jwt=token, key=setting.SECRET_KEY, algorithms=['HS256'])
