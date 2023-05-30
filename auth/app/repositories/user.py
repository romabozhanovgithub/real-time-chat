from boto3.dynamodb.conditions import Key
from community.repositories.dynamodb import BaseRepository


class UserRepository(BaseRepository):
    table_name = "users"
    partition_key = "username"

    async def create(self, item: dict) -> dict:
        return await self.put_item(item)

    async def get_by_username(self, username: str) -> dict:
        return await self.get_item(username)
    
    async def get_by_email(self, email: str) -> dict:
        response = await self.scan(
            filter_expression=Key("email").eq(email),
        )
        return response[0] if response else {}
