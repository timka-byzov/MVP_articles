from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CORS_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"


settings = Settings()