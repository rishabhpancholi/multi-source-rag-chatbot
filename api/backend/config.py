# Imports
from langsmith import Client

from pydantic_settings import BaseSettings,SettingsConfigDict

# Config class
class Config(BaseSettings):
    groq_api_key: str
    voyage_api_key: str
    postgres_user: str
    postgres_db: str
    postgres_password: str
    github_api_url: str
    github_personal_access_token: str
    langsmith_api_key: str

    model_config = SettingsConfigDict(env_file = ".env")

app_config = Config()

# Langsmith client
langsmith_client = Client(
    api_url = "https://api.smith.langchain.com",
    api_key = app_config.langsmith_api_key
)