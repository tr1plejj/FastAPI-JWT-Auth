from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # your secret key
ALGORITHM = 'HS256'
TOKEN_EXPIRES_MINUTES = 15
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
