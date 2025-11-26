from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
