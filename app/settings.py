from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        validate_default=False,
    )

    token: str

    @field_validator("token")
    @classmethod
    def token_must_not_be_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("token is required")
        return value
