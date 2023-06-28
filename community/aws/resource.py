import aioboto3
from mypy_boto3_dynamodb import ServiceResource


class AWSResource:
    _resource: ServiceResource | None = None

    def __init__(
        self,
        service_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_default_region: str,
        aws_endpoint_url: str | None = None,
    ) -> None:
        self.service_name = service_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_default_region = aws_default_region
        self.aws_endpoint_url = aws_endpoint_url

    @property
    def credentials(self) -> dict[str, str]:
        credentials = {
            "service_name": self.service_name,
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "aws_default_region": self.aws_default_region,
        }
        if self.aws_endpoint_url:
            credentials["endpoint_url"] = self.aws_endpoint_url
        return credentials
    
    async def _create_resource(self) -> ServiceResource:
        self._resource = await aioboto3.resource(
            **self.credentials
        )
        return self._resource
    
    async def close(self) -> None:
        await self._resource.close()
        self._resource = None

    async def __call__(self) -> ServiceResource:
        return await self._create_resource()
    
    async def __aenter__(self) -> ServiceResource:
        return await self._create_resource()
    
    async def __aexit__(self) -> None:
        await self.close()
