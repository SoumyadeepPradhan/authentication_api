from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from urllib.parse import quote_plus


env_path=Path(".")/".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    #Database
    DB_USER:str = os.getenv('MYSQL_USER')
    DB_PASSWORD:str = os.getenv('MYSQL_PASSWORD')
    DB_NAME:str = os.getenv('MYSQL_DB')
    DB_HOST:str = os.getenv('MYSQL_SERVER')
    DB_PORT:int = os.getenv('MYSQL_PORT')
    DB_URL:str = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}"

    #JWT
    JWT_SECRET:str = os.getenv('JWT_SECRET','f5a2ef1c8057dfa4e8b603f0aeb76fad8e405a19a32bc4339f62b3917a0de22b165b00656f424aa638cba7d8d146f3ac')
    JWT_ALGORITHM:str = os.getenv('JWT_ALGORITHM','HS256')
    ACCESS_TOKEN_EXPIRE_MUNUTES:int = os.getenv('ACCESS_TOKEN_EXPIRE_MUNUTES',60)

def get_settings()->Settings:
    return Settings()