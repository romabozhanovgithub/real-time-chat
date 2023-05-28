from community.repositories.dynamodb import BaseRepository


class UserRepository(BaseRepository):
    table_name = "users"
    partition_key = "username"

    async def create(self, item: dict) -> dict:
        return await self.put_item(item)
