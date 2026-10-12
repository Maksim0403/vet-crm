import os

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    debug: bool = False
    environment: str = "sandbox"

    model_config = SettingsConfigDict(env_file=f".env.{os.getenv('APP_ENV', 'sandbox')}")

    @model_validator(mode="after")
    def validate_production_safety(self):
        if self.environment == "production" and self.debug:
            raise ValueError("DEBUG must be False in production")
        return self


settings = Settings()
