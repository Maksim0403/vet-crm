from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str = "development-only-change-this-key"
    access_token_expire_minutes: int = 60
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin12345"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
