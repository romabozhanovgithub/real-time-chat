from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from community.core import settings as community_settings

from app.core.settings import settings

app = FastAPI(title=settings.APP_TITLE, debug=settings.DEBUG)
community_settings(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_default_region=settings.AWS_DEFAULT_REGION,
    aws_endpoint_url=settings.AWS_ENDPOINT_URL,
)


# MIDDLWARES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES


# EVENTS
@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass
