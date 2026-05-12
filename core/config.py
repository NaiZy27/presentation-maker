import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, RedisDsn

current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")


class Settings(BaseSettings):
    tg_bot_token: SecretStr
    redis_url: RedisDsn
    gemini_api_key: SecretStr
    unsplash_access_key: SecretStr
    allowed_user_id: int

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8",
        extra="ignore",
    )


config = Settings()
