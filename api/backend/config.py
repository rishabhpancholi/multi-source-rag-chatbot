# Imports
from pydantic_settings import BaseSettings,SettingsConfigDict

# Config class
class Config(BaseSettings):
    groq_api_key: str
    postgres_user: str
    postgres_db: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file = ".env")

app_config = Config()