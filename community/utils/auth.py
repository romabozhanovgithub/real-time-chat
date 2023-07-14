from datetime import datetime, timedelta
from jose import JWTError, jwt

from community.core import settings


def create_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT token with the given data and expiration time.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict | None:
    """
    Decode a JWT token and return the payload.
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
