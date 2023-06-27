class BaseSettings:
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    AWS_ENDPOINT_URL: str | None

    def __call__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_default_region: str,
        aws_endpoint_url: str | None = None,
    ) -> None:
        self.AWS_ACCESS_KEY_ID = aws_access_key_id
        self.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
        self.AWS_DEFAULT_REGION = aws_default_region
        self.AWS_ENDPOINT_URL = aws_endpoint_url


settings = BaseSettings()
