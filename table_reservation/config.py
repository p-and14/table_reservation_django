from pydantic import (
    Field, field_validator, HttpUrl,
    SecretStr, PostgresDsn, ValidationInfo
)
from pydantic_settings import BaseSettings, SettingsConfigDict

BAD_FORMAT = "Не верный формат {}."


class EnvDict(BaseSettings):
    """Подключаем env файл."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AppSettings(EnvDict):
    """Валидация настроек приложения."""
    DEBUG: bool
    SECRET_KEY: SecretStr=Field(
        ..., max_length=100,
        description="Длина SECRET_KEY не больше 100 знаков"
    )
    CORS_ALLOWED_ORIGINS: str=Field(..., description="Перечень хостов через запятую")

    @field_validator("CORS_ALLOWED_ORIGINS")
    def parse_cors_allowed_origins(cls, value: str) -> list[str]:
        """Строку в список доменов или субдоменов."""
        domains = [domain.strip() for domain in value.split(',')]
        for domain in domains:
            try:
                HttpUrl(domain)
            except ValueError:
                raise ValueError(BAD_FORMAT.format(domain))
        return value.split(',')


class PgSettings(EnvDict):
    """БД PostgreSQL: url + формирование url."""
    POSTGRES_DRV: str = "postgresql"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_URL: PostgresDsn | None = None

    @field_validator("POSTGRES_URL")
    def pg_url_validate(
        cls,
        value,
        values: ValidationInfo,
    ) -> PostgresDsn:
        data = values.data
        return PostgresDsn.build(
            scheme=data.get("POSTGRES_DRV"),
            username=data.get("POSTGRES_USER"),
            password=data.get("POSTGRES_PASSWORD").get_secret_value(),
            host=data.get("POSTGRES_HOST"),
            port=data.get("POSTGRES_PORT"),
            path=data.get("POSTGRES_DB"),
        )
    

app_settings = AppSettings()
DB_URL = str(PgSettings().POSTGRES_URL)
