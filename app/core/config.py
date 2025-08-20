from pydantic import BaseSettings, PostgresDsn, Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Spatial Data API"
    POSTGRES_DSN: PostgresDsn = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/spatial_db"
    )
    DB_ECHO: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
