from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from split_settings.tools import include

class Settings(BaseSettings):
    debug: bool = Field(False)
    secret_key: str
    allowed_hosts: list[str]

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()

SECRET_KEY = settings.secret_key
DEBUG = settings.debug
ALLOWED_HOSTS = settings.allowed_hosts

WSGI_APPLICATION = 'config.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

include(
    "components/application_definition.py",
    "components/auth_password_validators.py",
    "components/folders.py",
    "components/database.py",
    "components/internationalization.py",
    "components/drf.py",
)