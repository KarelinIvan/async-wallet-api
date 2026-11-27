from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Глобальные настройки приложения."""

    # (драйвер/диалект, учётные данные, хост и порт, имя базы данных)
    DATABASE_URL: str
    # Для тестовой БД (драйвер/диалект, учётные данные, хост и порт, имя базы данных)
    TEST_DATABASE_URL: str
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
