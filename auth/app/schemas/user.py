from pydantic import BaseModel, EmailStr, Field
from community.schemas.base import BaseConfig

from app.core.utils import generate_uuid


class UserTableSchema(BaseModel):
    id: str = Field(..., default_factory=generate_uuid)
    username: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(..., min_length=8)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config(BaseConfig):
        pass


class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config(BaseConfig):
        pass
