from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MODEL_PROVIDER = "openai"
DEFAULT_MODEL_NAME = "gpt-4.1-mini"


@dataclass(frozen=True)
class Settings:
    app_env: str
    model_provider: str
    model_name: str
    openai_api_key: str | None
    anthropic_api_key: str | None
    gemini_api_key: str | None
    azure_openai_api_key: str | None
    azure_openai_endpoint: str | None
    telegram_bot_token: str | None
    whatsapp_access_token: str | None
    whatsapp_phone_number_id: str | None

    def require(self, name: str) -> str:
        value = getattr(self, name)
        if not value:
            env_name = name.upper()
            raise RuntimeError(f"Missing required secret/config value: {env_name}")
        return value


def load_settings(env_file: str | Path | None = None) -> Settings:
    if env_file is not None:
        load_env_file(env_file)

    return Settings(
        app_env=_get("APP_ENV", "development"),
        model_provider=_get("MODEL_PROVIDER", DEFAULT_MODEL_PROVIDER),
        model_name=_get("MODEL_NAME", DEFAULT_MODEL_NAME),
        openai_api_key=_get("OPENAI_API_KEY"),
        anthropic_api_key=_get("ANTHROPIC_API_KEY"),
        gemini_api_key=_get("GEMINI_API_KEY"),
        azure_openai_api_key=_get("AZURE_OPENAI_API_KEY"),
        azure_openai_endpoint=_get("AZURE_OPENAI_ENDPOINT"),
        telegram_bot_token=_get("TELEGRAM_BOT_TOKEN"),
        whatsapp_access_token=_get("WHATSAPP_ACCESS_TOKEN"),
        whatsapp_phone_number_id=_get("WHATSAPP_PHONE_NUMBER_ID"),
    )


def load_env_file(path: str | Path) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = _clean_env_value(value.strip())

        if key and key not in os.environ:
            os.environ[key] = value


def _get(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def _clean_env_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
