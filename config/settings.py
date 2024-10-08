import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # App
    APP_NAME:  str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))
    
    # FrontEnd Application
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:8000")

    # Postgresql Database Config
    POSTGRE_HOST: str = os.environ.get("POSTGRE_HOST")
    POSTGRE_USER: str = os.environ.get("POSTGRE_USER")
    POSTGRE_PASS: str = os.environ.get("POSTGRE_PASS")
    POSTGRE_PORT: int = int(os.environ.get("POSTGRE_PORT"))
    POSTGRE_DB: str = os.environ.get("POSTGRE_DB")
    DATABASE_URI: str = f"postgresql+psycopg2://{POSTGRE_USER}:{POSTGRE_PASS}@{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_DB}"

    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")


@lru_cache()
def get_settings() -> Settings:
    return Settings()