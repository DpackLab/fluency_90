from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Configuración de Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignora variables de entorno que no estén definidas aquí
    )

    # Datos generales de la app
    APP_NAME: str = Field(default="Fluency_90 Backend V2")
    APP_ENV: str = Field(default="dev")

    # Parámetros de conexión a PostgreSQL
    POSTGRES_USER: str = Field(default="fluency90_user")
    POSTGRES_PASSWORD: str = Field(default="change_me")
    POSTGRES_DB: str = Field(default="fluency90_db")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)

    # Parámetros de JWT
    JWT_SECRET_KEY: str = Field(
        default="change_this_secret_key",
        description="Llave secreta para firmar los tokens JWT.",
    )
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """
        URL síncrona: la usa el motor síncrono (psycopg2) y Alembic.
        """
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """
        URL asíncrona: la usará el backend cuando montemos motor async (asyncpg).
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Instancia global de configuración
settings = Settings()
