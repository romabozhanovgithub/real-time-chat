from mypy_boto3_dynamodb.service_resource import Table

from app.core.aws.client import AWSClient


class DynamoDB(AWSClient):
    service_name = "dynamodb"
    table_name: str
    _table: Table | None = None

    @property
    def table(self) -> Table:
        if self._table is None:
            self._table = self.resource.Table(self.table_name)
        return self._table
