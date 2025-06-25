from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    DATABASE_URL: str = Field(default="sqlite:///./app.db", env="DATABASE_URL")
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "https://lboy2006.github.io/fletapp1",
            "https://lboy2006.github.io"
        ],
        env="CORS_ORIGINS",
    )
    TELEGRAM_BOT_TOKEN: str = Field(default="", env="TELEGRAM_BOT_TOKEN")
    LAVA_API_KEY: str = Field(default="", env="LAVA_API_KEY")
    LAVA_OFFER_ID: str = Field(default="78fd63a5-1ed5-4f55-900d-b01bf16b6593", env="LAVA_OFFER_ID")
    TEST_MODE: bool = Field(default=False, env="TEST_MODE")
    class Config:
        env_file = ".env"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors_origins(cls, v: str | List[str]) -> List[str]:
        return cls.parse_cors_origins(v)

    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
