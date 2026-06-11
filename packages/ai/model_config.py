from __future__ import annotations
from dataclasses import dataclass
from packages.shared.config import Settings, load_settings


SUPPORTED_MODEL_PROVIDERS = {"azure", "azure_openai", "gemini", "google", "openai"}


@dataclass(frozen=True)
class AzureOpenAIModelConfig:
    api_key: str
    endpoint: str
    api_version: str
    deployment: str
    model_name: str


@dataclass(frozen=True)
class GeminiModelConfig:
    api_key: str
    model_name: str


# Normalizes provider aliases into the names used by this package.
def normalize_model_provider(provider: str) -> str:
    normalized = provider.strip().lower().replace("-", "_")

    if normalized == "google":
        return "gemini"
    if normalized == "azure_openai":
        return "azure"

    if normalized not in SUPPORTED_MODEL_PROVIDERS:
        supported = ", ".join(sorted(SUPPORTED_MODEL_PROVIDERS))
        raise ValueError(f"Unsupported model provider '{provider}'. Use one of: {supported}")

    return normalized


# Loads and validates all settings required for Azure OpenAI.
def get_azure_openai_config(settings: Settings | None = None) -> AzureOpenAIModelConfig:
    if settings is None:
        settings = load_settings()

    api_key = settings.require("azure_openai_api_key")
    endpoint = settings.require("azure_openai_endpoint")
    api_version = settings.require("azure_openai_api_version")
    deployment = settings.azure_openai_deployment or settings.model_name

    if not deployment:
        raise RuntimeError(
            "Missing required secret/config value: AZURE_OPENAI_DEPLOYMENT or MODEL_NAME"
        )

    return AzureOpenAIModelConfig(
        api_key=api_key,
        endpoint=endpoint.rstrip("/"),
        api_version=api_version,
        deployment=deployment,
        model_name=settings.model_name,
    )


# Loads and validates all settings required for Gemini.
def get_gemini_config(settings: Settings | None = None) -> GeminiModelConfig:
    if settings is None:
        settings = load_settings()

    return GeminiModelConfig(
        api_key=settings.require("gemini_api_key"),
        model_name=settings.model_name,
    )


# Returns the validated config object for the selected model provider.
def get_model_config(settings: Settings | None = None) -> AzureOpenAIModelConfig | GeminiModelConfig:
    if settings is None:
        settings = load_settings()

    provider = normalize_model_provider(settings.model_provider)

    if provider == "azure":
        return get_azure_openai_config(settings)
    if provider == "gemini":
        return get_gemini_config(settings)

    raise ValueError(
        f"Provider '{settings.model_provider}' does not have a client config helper yet"
    )


__all__ = [
    "AzureOpenAIModelConfig",
    "GeminiModelConfig",
    "SUPPORTED_MODEL_PROVIDERS",
    "get_azure_openai_config",
    "get_gemini_config",
    "get_model_config",
    "normalize_model_provider",
]
