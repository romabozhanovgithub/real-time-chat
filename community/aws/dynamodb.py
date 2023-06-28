from community.aws.client import AWSClient


class DynamoDB(AWSClient):
    service_name = "dynamodb"


dynamodb = DynamoDB()
