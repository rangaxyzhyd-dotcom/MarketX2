from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    SECRET_KEY: str = "dev-only-change-me"
    DATABASE_URL: str = "sqlite:///./marketx.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
