from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    SECRET_KEY: str
    APP_TITLE: str = "Auth Service"
    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str


settings = Settings()
