from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""

    # Change this if the Gemini model available to your API account differs.
    gemini_model: str = "gemini-3.8-flash"

    # auto   = try local LaMini, then Gemini
    # local  = use local LaMini only
    # gemini = use Gemini only
    explanation_backend: str = "auto"

    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"

    local_model_max_new_tokens: int = 256

    # Useful when developing the frontend without an API key.
    demo_mode: bool = False

    max_input_chars: int = 20000

    request_timeout_seconds: float = 60.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()