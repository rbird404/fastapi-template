from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str

    JWT_EXP: int = 5  # minutes
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days


auth_config = AuthConfig()
