from typing import Any, Literal
from aioboto3.dynamodb.table import BatchWriter
from boto3.dynamodb.conditions import ConditionBase
from mypy_boto3_dynamodb.service_resource import Table

from community.aws import AWSResource, DynamoDB, dynamodb
from community.core.types import (
    ItemTable,
    QueryTable,
    QueryTableResponse,
    ScanTable,
    ScanTableResponse
)


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

    def __create_params(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params
    
    def __create_primary_key(
            self, partition_key: str, sort_key: str | None = None
        ) -> dict[str, str]:
        key = {self.partition_key: partition_key}
        if sort_key:
            key[self.sort_key] = sort_key
        return key
    
    async def _paginate(
        self,
        method: QueryTable | ScanTable,
        response: QueryTableResponse | ScanTableResponse,
        **kwargs
    ) -> QueryTableResponse | ScanTableResponse:
        items = response.get("Items")
        while response.get("LastEvaluatedKey"):
            kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = await method(**kwargs)
            items.extend(response["Items"])
        response["Items"] = items
        return response

    async def _get_all_items(
        self,
        method: QueryTable | ScanTable,
        **kwargs
    ) -> QueryTableResponse | ScanTableResponse:
        response = await method(**kwargs)
        self._paginate(method, response, **kwargs)
        return response
    
    async def _get_items(
        self,
        method: QueryTable | ScanTable,
        all_items: bool = False,
        **kwargs
    ) -> QueryTableResponse | ScanTableResponse:
        if all_items:
            return await self._get_all_items(method, **kwargs)
        response = await method(**kwargs)
        return response

    async def put_item(
        self, item: ItemTable
    ) -> dict:
        await self.table.put_item(Item=item)
        return item

    async def get_item(
        self, partition_key: str, sort_key: str | None = None
    ) -> ItemTable:
        key = self.__create_primary_key(partition_key, sort_key)
        response: ItemTable = await self.table.get_item(Key=key)
        return response.get("Item", {})
    
    async def _query(
        self,
        key_condition_expression: ConditionBase,
        index_name: str | None = None,
        select: str | None = None,
        filter_expression: ConditionBase | None = None,
        order: Literal["ASC", "DESC"] = "ASC",
        exclude_start_key: Any | None = None,
        all_items: bool = False,
    ) -> QueryTableResponse:
        kwargs = self.__create_params(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select,
            FilterExpression=filter_expression,
            ExclusiveStartKey=exclude_start_key,
            ScanIndexForward=order == "ASC",
        )
        return await self._get_items(
            self.table.query, all_items, **kwargs
        )

    async def query(
        self,
        key_condition_expression: ConditionBase,
        index_name: str | None = None,
        select: str | None = None,
        filter_expression: ConditionBase | None = None,
        order: Literal["ASC", "DESC"] = "ASC",
        exclude_start_key: Any | None = None,
        all_items: bool = False,
    ) -> list[ItemTable]:
        response = await self._query(
            key_condition_expression,
            index_name,
            select,
            filter_expression,
            order,
            exclude_start_key,
            all_items,
        )
        return response.get("Items", [])
    
    async def _scan(
        self,
        filter_expression: ConditionBase | None = None,
        select: str | None = None,
        all_items: bool = False,
    ) -> ScanTableResponse:
        kwargs = self.__create_params(
            FilterExpression=filter_expression,
            Select=select,
        )
        return await self._get_items(
            self.table.scan, all_items, **kwargs
        )

    async def scan(
        self,
        filter_expression: ConditionBase | None = None,
        select: str | None = None,
        all_items: bool = False,
    ) -> list[ItemTable]:
        response = await self._scan(
            filter_expression,
            select,
            all_items,
        )
        return response.get("Items", [])

    async def put_item(self, item: ItemTable) -> ItemTable:
        await self.table.put_item(Item=item)
        return item

    async def delete_item(
        self, partition_key: str, sort_key: str | None = None
    ) -> None:
        key = self.__create_primary_key(partition_key, sort_key)
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
        self._resource = None
        self._table = None
