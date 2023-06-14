import re
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def validate_username(username: str) -> bool:
    return bool(re.fullmatch(r'^[\w_]*$', username))
