from aioboto3.dynamodb.table import BatchWriter
from mypy_boto3_dynamodb.service_resource import Table

from app.core.aws.client import AWSClient


class DynamoDB(AWSClient):
    service_name = "dynamodb"
    table_name: str
    _table: Table | None = None
    batch_writer: BatchWriter | None = None

    def __init__(self) -> None:
        self.batch_writer = self.table.batch_writer()

    @property
    def table(self) -> Table:
        if self._table is None:
            self._table = self.resource.Table(self.table_name)
        return self._table
