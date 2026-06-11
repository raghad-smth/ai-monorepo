from __future__ import annotations
from packages.ai.model_config import GeminiModelConfig, get_gemini_config
from packages.shared.config import Settings, load_settings


# Creates a Gemini SDK client from validated settings.
def create_gemini_client(settings: Settings | None = None):
    config = get_gemini_config(settings)

    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "Gemini support requires the google-genai package. "
            "Install it with: pip install google-genai"
        ) from exc

    return genai.Client(api_key=config.api_key)


# Returns the Gemini model name used for model calls.
def get_default_gemini_model(settings: Settings | None = None) -> str:
    if settings is None:
        settings = load_settings()
    return get_gemini_config(settings).model_name


__all__ = ["GeminiModelConfig", "create_gemini_client", "get_default_gemini_model"]
