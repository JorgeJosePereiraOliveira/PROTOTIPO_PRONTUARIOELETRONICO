from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    CONNECTION: str = Field(..., env="CONNECTION")


settings = Settings()
