from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str
    PORT: int
    SECRET_KEY: SecretStr
    DATABASE_URL: PostgresDsn
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    CORS_ALLOWED_ORIGINS: list[str]

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def async_database_url(self):
        # postgresql+asyncpg://user:password@localhost:5432/db_name
        return str(self.DATABASE_URL)

    @property
    def secret_key_str(self):
        return str(self.SECRET_KEY)


settings = Settings()
