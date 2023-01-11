from bcrypt import checkpw, gensalt, hashpw


def generate_password(password: str) -> str:
    return hashpw(password=password.encode('utf-8'), salt=gensalt()).decode('utf-8')


def validate_password(password: str, hash_password: str) -> bool:
    return checkpw(password=password.encode('utf-8'), hashed_password=hash_password.encode('utf-8'))
