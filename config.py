from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str

    class Config:
        env_file = ".env"
