import aioboto3
from mypy_boto3_dynamodb import ServiceResource

from app.core import settings


class AWSClient:
    service_name: str
    _resource: ServiceResource | None = None

    @property
    def credentials(self) -> dict[str, str]:
        credentials = {
            "service_name": self.service_name,
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "AWS_DEFAULT_REGION": settings.AWS_DEFAULT_REGION,
        }
        if settings.AWS_ENDPOINT_URL:
            credentials["endpoint_url"] = settings.AWS_ENDPOINT_URL
        return credentials

    @property
    def resource(self) -> ServiceResource:
        if self._resource is None:
            self._resource: ServiceResource = aioboto3.resource(
                **self.credentials
            )
        return self._resource
