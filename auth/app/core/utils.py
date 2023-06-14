import re
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def validate_username(username: str) -> bool:
    return bool(re.fullmatch(r'^[\w_]*$', username))


def validate_password(password: str) -> bool:
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
    return bool(password_regex.match(password))
