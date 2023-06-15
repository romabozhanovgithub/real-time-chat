from boto3.dynamodb.conditions import Key
from community.repositories.dynamodb import BaseRepository
from community.core.types import ItemTable

from app.schemas import UserTableSchema


class UserRepository(BaseRepository):
    """
    This class is responsible for operations on the user table
    """

    table_name = "users"
    partition_key = "username"

    async def create(self, item: ItemTable) -> UserTableSchema:
        """
        Create a new user
        """

        response = await self.put_item(item)
        return UserTableSchema(**response)

    async def get_by_username(self, username: str) -> UserTableSchema | None:
        """
        Get a user by username
        """

        response = await self.get_item(partition_key=username)
        return UserTableSchema(**response) if response else None

    async def get_by_email(self, email: str) -> UserTableSchema | None:
        """
        Get a user by email
        """

        response = await self.scan(
            filter_expression=Key("email").eq(email),
        )
        return UserTableSchema(**response[0]) if response else None

    async def update(
        self,
        username: str,
        item: ItemTable,
    ) -> UserTableSchema:
        """
        Update a user by username
        """

        response = await self.update_item(
            partition_key=username,
            data=item,
        )
        return UserTableSchema(**response)

    async def delete(self, username: str) -> None:
        """
        Delete a user by username
        """

        return await self.delete_item(partition_key=username)
