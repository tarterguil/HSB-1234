import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "HARNESS AI AGENTIC"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DEEPSEEK_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    DEFAULT_DIRECTOR_MODEL: str = "deepseek/deepseek-chat"
    DEFAULT_SCENARIO_MODEL: str = "google/gemini-2.5-flash"
    DEFAULT_VISUAL_MODEL: str = "qwen/qwen-2.5-72b-instruct"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
