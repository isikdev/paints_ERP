from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Class that retrieves settings from dotenv file."""
    app_name: str = 'Paints ERP'
    echo_sql: bool = True
    test: bool = False
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=('.env', '../.env', ), extra='allow')


@lru_cache
def get_settings() -> Settings:
    """Returns Settings instance."""
    return Settings()
