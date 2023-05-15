from typing import Callable, Literal
from boto3.dynamodb.conditions import ConditionBase

from app.core.aws import DynamoDB


class BaseRepository(DynamoDB):
    table_name: str
    partition_key: str
    sort_key: str | None = None

    async def create(self, item: dict) -> dict:
        await self.table.put_item(Item=item)
        return item

    async def get(
        self, partition_key: str, sort_key: str | None = None
    ) -> dict:
        key = {self.partition_key: partition_key}
        if sort_key:
            key[self.sort_key] = sort_key
        response = await self.table.get_item(Key=key)
        return response.get("Item", {})
