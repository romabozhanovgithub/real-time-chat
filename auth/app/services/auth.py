from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.dependencies import get_user_repository
from app.core.utils import validate_password
from app.core.exceptions import PasswordsDoNotMatchException, InvalidPasswordException
from app.repositories import UserRepository
from app.schemas import SignUpRequestSchema, UserResponseSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    This class is responsible for operations on the user table
    """

    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends(get_user_repository)):
        self.user_repository = user_repository
        
    def _verify_password(plain_password, hashed_password) -> bool:
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
