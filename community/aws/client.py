from mypy_boto3_dynamodb import ServiceResource

from community.core import settings
from community.aws.resource import AWSResource


class AWSClient:
    service_name: str

    @property
    def credentials(self) -> dict[str, str]:
        credentials = {
            "service_name": self.service_name,
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "aws_default_region": settings.AWS_DEFAULT_REGION,
        }
        if settings.AWS_ENDPOINT_URL:
            credentials["endpoint_url"] = settings.AWS_ENDPOINT_URL
        return credentials
    
    @property
    def resource(self) -> ServiceResource:
        return AWSResource(**self.credentials)
