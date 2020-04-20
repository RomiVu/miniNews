import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TEST = os.getenv("TEST", False)
    ENV = os.getenv("ENV", 'dev')
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./default.db")
    SECRET_KEY = '52839a307fc6308425752ce01a302e4c797a1d62e93cd3e2d3c83af06786a648'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300


class Base(BaseSettings):
    TEST = False
    DATABASE_URL = "sqlite:///./default.db"
    SECRET_KEY = '52839a307fc6308425752ce01a302e4c797a1d62e93cd3e2d3c83af06786a648'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

class DevSetting(Base):
    pass

class ProdSetting(Base):
    DATABASE_URL = "postgresql+psycopg2://looooke:123456lk@@@localhost/dev"

class TestSetting(Base):
    TEST = True


setting = Settings()