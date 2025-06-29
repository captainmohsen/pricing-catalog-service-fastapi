import secrets
import logging
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import SettingsConfigDict,BaseSettings
import os

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 8))
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST", "https://localhost")

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS", ["http://localhost:4200"])

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Pricing Service")

    #postgres db settings
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER","pricing-db")
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER","postgres")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD","root1234")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB","pricing_db")
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql+asyncpg://postgres:root1234@db:5432/pricing_db",
    )
    SQLALCHEMY_SYNC_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://postgres:root1234@db:5432/pricing_db",
    )
    connect_args: dict = os.getenv("connect_args", {"server_settings": {"options": "-c timezone=UTC", "timezone": "UTC"}})

    #redis settings
    REDIS_SERVER: str = os.getenv("REDIS_SERVER", "redis:6379/0")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")

    REDIS_BROKER_URL: str = "redis://redis:6379/0"
    # redis_result_backend: str = "redis://localhost:6379/1"


    TEST_USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD", "Test@123")
    TEST_USER_EMAIL: EmailStr = os.getenv("TEST_USER_EMAIL", "info@socialbot.com")
    TEST_USER_USERNAME: str = os.getenv("FIRST_SUPER_ADMIN_USERNAME", "test_user")
    DOMAIN: str = os.getenv("DOMAIN", "")
    TZ: str = os.getenv("TZ", "UTC")




    NETWORK_SERVICE_URL:str = ""
    REGION_SERVICE_URL:str = ""
    IMAGE_SERVICE_URL : str = ""
    VOLUME_SERVICE_URL: str = ""
    IAM_SERVICE_URL: str = ""

    model_config = SettingsConfigDict(case_sensitive=True)



settings = Settings()