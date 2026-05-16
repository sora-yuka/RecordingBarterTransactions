from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    secret_key: SecretStr = Field(alias="SECRET_KEY")
    database_url: PostgresDsn = Field(alias="DATABASE_URL")

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()