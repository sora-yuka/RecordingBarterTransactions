from src.utils.get_env_file import find_env_file

from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    secret_key: SecretStr = Field(alias="SECRET_KEY")
    DATABASE_URL: PostgresDsn

    model_config = SettingsConfigDict(env_file=find_env_file())

    @property
    def async_database_url(self):
        # postgresql+asyncpg://user:password@localhost:5432/db_name
        return str(self.DATABASE_URL)


settings = Settings()
