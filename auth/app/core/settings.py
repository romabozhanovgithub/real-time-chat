from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    SECRET_KEY: str
    APP_TITLE: str = "Auth Service"
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    AWS_ENDPOINT_URL: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
