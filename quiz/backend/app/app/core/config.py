import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    # url naming: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlite
    HOST: str
    PORT: str

    WORKERS_PER_CORE: int = 1
    WEB_CONCURRENCY: str | None
    SQLALCHEMY_DATABASE_URL: str
    BEARER_TOKEN: str
    COUNT_TESTS_SERVICES: int
    REQUESTS_EXPIRATION_TIME_IN_MINUTES: int
    LOG_LEVEL: str = "error"

    TEST_SERVICES_BEARER_TOKEN: str
    TEST_SERVICE_URL: str

    BURNOUT_SERVICE_NAME: str
    BURNOUT_SERVICE_URL: str

    FATIGUE_SERVICE_NAME: str
    FATIGUE_SERVICE_URL: str

    COPING_SERVICE_NAME: str
    COPING_SERVICE_URL: str

    SPB_SERVICE_NAME: str
    SPB_SERVICE_URL: str

    QUESTIONNAIRE_SERVICE_NAME: str
    QUESTIONNAIRE_SERVICE_URL: str

    TOKEN_SERVICE_URL: str

    class Config:
        # case_sensitive: https://docs.pydantic.dev/usage/settings/#environment-variable-names
        case_sensitive = True

        # read settings from .env file
        env_file = "..env"
        env_file_encoding = 'utf-8'


settings = Settings(_env_file=f'{pathlib.Path(__file__).parents[3].resolve()}/.env')
