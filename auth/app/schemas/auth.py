from typing import Any
from pydantic import BaseModel, EmailStr, Field, validator
from community.schemas.base import BaseConfig

from app.core.utils import generate_uuid, validate_password, validate_username
from app.core.exceptions import (
    InvalidUsernameException,
    PasswordsDoNotMatchException,
    InvalidPasswordException,
)


class SignUpRequestSchema(BaseModel):
    id: str | None = Field(default_factory=generate_uuid)
    username: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    class Config(BaseConfig):
        pass
