from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"


class ElasticSettings(BaseSettings): 
    port: int = 9200
    url: str = "http://0.0.0.0"
    username: str = "user"
    password: str = "password"

    hosts: str = f"{url}:{port}"

    model_config = SettingsConfigDict(env_prefix='elastic_')

    # class Config:
    #     env_file = ".env"


settings = Settings()
elastic_settings = ElasticSettings()
