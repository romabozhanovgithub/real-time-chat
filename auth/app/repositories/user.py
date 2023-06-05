from boto3.dynamodb.conditions import Key
from community.repositories.dynamodb import BaseRepository
from community.core.types import ItemTable


class UserRepository(BaseRepository):
    table_name = "users"
    partition_key = "username"

    async def create(self, item: ItemTable) -> ItemTable:
        """
        Create a new user
        """

        return await self.put_item(item)

    async def get_by_username(self, username: str) -> ItemTable:
        """
        Get a user by username
        """

        return await self.get_item(partition_key=username)
    
    async def get_by_email(self, email: str) -> ItemTable:
        """
        Get a user by email
        """

        response = await self.scan(
            filter_expression=Key("email").eq(email),
        )
        return response[0] if response else {}
    
    async def update(
        self,
        username: str,
        **kwargs: ItemTable,
    ) -> ItemTable:
        return await self.update_item(
            partition_key=username,
            **kwargs,
        )
    
    async def delete(self, username: str) -> ItemTable:
        return await self.delete_item(partition_key=username)
