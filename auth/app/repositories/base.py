from typing import Callable, Literal
from boto3.dynamodb.conditions import ConditionBase

from app.core.aws import DynamoDB


class BaseRepository(DynamoDB):
    table_name: str
    partition_key: str
    sort_key: str | None = None
