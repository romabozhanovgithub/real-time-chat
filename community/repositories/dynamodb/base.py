from typing import Any, Callable, Literal
from aioboto3.dynamodb.table import BatchWriter
from boto3.dynamodb.conditions import ConditionBase
from mypy_boto3_dynamodb.service_resource import Table

from community.aws import AWSResource, DynamoDB, dynamodb


class BaseRepository:
    table_name: str
    partition_key: str
    sort_key: str | None = None
    dynamodb: DynamoDB = dynamodb
    _resource: AWSResource | None = None
    _table: Table | None = None
    _batch_writer: BatchWriter | None = None

    @property
    def table(self) -> Table:
        if self._table is None:
            raise Exception("Table is None")
        return self._table
    
    @property
    def batch_writer(self) -> BatchWriter:
        if self._batch_writer is None:
            self._batch_writer = self.table.batch_writer()
        return self._batch_writer

    def _create_params(self, **kwargs: dict) -> dict:
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params

    async def _get_all_items(self, method: Callable, **kwargs) -> list[dict]:
        response = await method(**kwargs)
        items: list = response["Items"]
        while "LastEvaluatedKey" in response:
            kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = await method(**kwargs)
            items.extend(response["Items"])
        return items
    
    async def _get_items(
        self,
        method: Callable,
        all_items: bool = False,
        **kwargs
    ) -> list[dict]:
        if all_items:
            return await self._get_all_items(method, **kwargs)
        response = await method(**kwargs)
        return response["Items"]

    async def put_item(
        self, item: dict
    ) -> dict:
        await self.table.put_item(Item=item)
        return item

    async def get_item(
        self, partition_key: str, sort_key: str | None = None
    ) -> dict:
        key = {self.partition_key: partition_key}
        if sort_key:
            key[self.sort_key] = sort_key
        response: dict = await self.table.get_item(Key=key)
        return response.get("Item", {})

    async def query(
        self,
        key_condition_expression: ConditionBase,
        index_name: str | None = None,
        select: str | None = None,
        filter_expression: ConditionBase | None = None,
        order: Literal["ASC", "DESC"] = "ASC",
        exclude_start_key: Any | None = None,
        limit: int | None = None,
        all_items: bool = False,
    ) -> list[dict]:
        kwargs = self._create_params(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select,
            FilterExpression=filter_expression,
            ExclusiveStartKey=exclude_start_key,
            ScanIndexForward=order == "ASC",
            Limit=limit,
        )
        return await self._get_items(
            self.table.query, all_items, **kwargs
        )

    async def scan(
        self,
        filter_expression: ConditionBase | None = None,
        select: str | None = None,
        limit: int | None = None,
        all_items: bool = False,
    ) -> list[dict]:
        kwargs = self._create_params(
            FilterExpression=filter_expression,
            Select=select,
            Limit=limit,
        )
        return await self._get_items(
            self.table.scan, all_items, **kwargs
        )

    async def put_item(self, item: dict) -> dict:
        await self.table.put_item(Item=item)
        return item

    async def delete_item(
        self, partition_key: str, sort_key: str | None = None
    ) -> None:
        key = {self.partition_key: partition_key}
        if sort_key:
            key[self.sort_key] = sort_key
        await self.table.delete_item(Key=key)

    async def delete_items(self, key_expression: list[dict]) -> None:
        async with self.batch_writer as batch:
            for key in key_expression:
                await batch.delete_item(Key=key)

    async def __aenter__(self) -> None:
        self._resource = await self.dynamodb.resource()
        self._table = await self._resource.Table(self.table_name)
    
    async def __aexit__(self) -> None:
        await self._resource.close()
        self._table = None
