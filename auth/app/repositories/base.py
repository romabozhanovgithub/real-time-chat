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

    async def _get_all_items(self, method: Callable, **kwargs) -> list[dict]:
        response = await method(**kwargs)
        items: list = response["Items"]
        while "LastEvaluatedKey" in response:
            kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = await method(**kwargs)
            items.extend(response["Items"])
        return items

    async def query(
        self,
        key_condition_expression: ConditionBase,
        index_name: str | None = None,
        select: str | None = None,
        filter_expression: ConditionBase | None = None,
        order: Literal["ASC", "DESC"] = "ASC",
        limit: int | None = None,
        all_items: bool = False,
    ) -> list[dict]:
        kwargs = {
            "KeyConditionExpression": key_condition_expression,
            "IndexName": index_name,
            "Select": select,
            "FilterExpression": filter_expression,
            "ScanIndexForward": order == "ASC",
            "Limit": limit,
        }
        if all_items:
            return await self._get_all_items(self.table.query, **kwargs)
        response = await self.table.query(**kwargs)
        return response["Items"]

    async def scan(
        self,
        filter_expression: ConditionBase | None = None,
        select: str | None = None,
        limit: int | None = None,
        all_items: bool = False,
    ) -> list[dict]:
        kwargs = {
            "Select": select,
            "FilterExpression": filter_expression,
            "Limit": limit,
        }
        if all_items:
            return await self._get_all_items(self.table.scan, **kwargs)
        response = await self.table.scan(**kwargs)
        return response["Items"]

    async def update(self, item: dict) -> dict:
        await self.table.put_item(Item=item)
        return item

    async def delete(
        self, partition_key: str, sort_key: str | None = None
    ) -> None:
        key = {self.partition_key: partition_key}
        if sort_key:
            key[self.sort_key] = sort_key
        await self.table.delete_item(Key=key)

    async def delete_items(self, filter_expression: list) -> None:
        kwargs = {"FilterExpression": filter_expression}
        async with self.batch_writer:
            async for item in self.scan(**kwargs):
                await self.batch_writer.delete_item(
                    Key={self.partition_key: item[self.partition_key]}
                )
