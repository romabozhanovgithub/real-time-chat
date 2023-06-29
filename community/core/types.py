from decimal import Decimal
from typing import Any, Mapping, Sequence, Set, Union
from mypy_boto3_dynamodb.type_defs import (
    QueryOutputTableTypeDef,
    ScanOutputTableTypeDef,
)

ItemTable = Mapping[
    str,
    Union[
        bytes,
        bytearray,
        str,
        int,
        Decimal,
        bool,
        Set[int],
        Set[Decimal],
        Set[str],
        Set[bytes],
        Set[bytearray],
        Sequence[Any],
        Mapping[str, Any],
        None,
    ],
]

QueryTableResponse = dict | QueryOutputTableTypeDef
ScanTableResponse = dict | ScanOutputTableTypeDef


class QueryTable:
    async def __call__(self, *args: Any, **kwds: Any) -> QueryOutputTableTypeDef:
        pass


class ScanTable:
    async def __call__(self, *args: Any, **kwds: Any) -> ScanOutputTableTypeDef:
        pass
