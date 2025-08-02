from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    JWT_SECRET: str = "7f09c322de54a7fa860588fa70f2b86cf1a89b22f3294976bc8bdfbacae06d04"

settings = Settings()
