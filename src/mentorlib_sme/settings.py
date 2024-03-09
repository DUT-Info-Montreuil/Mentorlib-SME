from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    pg_user: str = ""
    pg_password: SecretStr = ""
    pg_host: str = ""
    pg_port: int = 5432
    pg_db: str = ""

    flask_secret: SecretStr = "secret"


settings = AppSettings()
