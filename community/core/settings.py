class BaseSettings:
    SECRET_KEY: str | None
    ALGORITHM: str | None

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    AWS_ENDPOINT_URL: str | None

    def __call__(
        self,
        secret_key: str | None = None,
        algorithm: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_default_region: str | None = None,
        aws_endpoint_url: str | None = None,
    ) -> None:
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.AWS_ACCESS_KEY_ID = aws_access_key_id
        self.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
        self.AWS_DEFAULT_REGION = aws_default_region
        self.AWS_ENDPOINT_URL = aws_endpoint_url


settings = BaseSettings()
