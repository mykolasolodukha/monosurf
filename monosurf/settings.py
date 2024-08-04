"""Settings for the project."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the project."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="MONOSURF__")

    API_KEY_HEADER_NAME: str = "X-API-Key"

    DEFAULT_CURRENCY_SYMBOL: str = "UAH"
    DEFAULT_CURRENCY_CODE: int = 980

    DEFAULT_COMMENT: str | None = None


settings = Settings()
