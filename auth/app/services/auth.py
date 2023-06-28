from fastapi import Depends
from passlib.context import CryptContext
from community.utils import create_token

from app.core.dependencies import get_user_repository
from app.core.exceptions import LoginException
from app.repositories import UserRepository
from app.schemas import (
    SignUpRequestSchema,
    UserResponseSchema,
    UserTableSchema,
    AccessTokenResponseSchema
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    This class is responsible for operations on the user table
    """

    user_repository: UserRepository

    def __init__(
        self, user_repository: UserRepository = Depends(get_user_repository)
    ) -> None:
        self.user_repository = user_repository
        
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify the password
        """

        return pwd_context.verify(plain_password, hashed_password)
    
    def _hash_password(password: str) -> str:
        """
        Create a hash of the password
        """

        return pwd_context.hash(password)

    async def sign_up(self, user: SignUpRequestSchema) -> UserResponseSchema:
        """
        Create a new user
        """

        response = await self.user_repository.create({
            **user.dict(
                by_alias=True,
                exclude={"password", "confirm_password"}
            ),
            "password": self._hash_password(user.password)
        })
        return response
    
    async def login(
        self, username: str, password: str
    ) -> AccessTokenResponseSchema:
        """
        Login a user with username and password
        """

        user: UserTableSchema = await self.user_repository.get_by_username(
            username
        )
        
        if not (user or self._verify_password(password, user.password)):
            raise LoginException()
        
        access_token = create_token({"username": user.username})
        return AccessTokenResponseSchema(access_token=access_token)
