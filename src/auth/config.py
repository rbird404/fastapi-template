from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str

    JWT_EXP: int = 5  # minutes
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


auth_config = AuthConfig()
