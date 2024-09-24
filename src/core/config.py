import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class EngineConfig(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 5


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    engine_config: EngineConfig = EngineConfig()
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__"
    )


settings = Settings()


def get_db_url() -> str:
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
