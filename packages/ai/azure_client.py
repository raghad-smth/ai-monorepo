from __future__ import annotations
from packages.ai.model_config import AzureOpenAIModelConfig, get_azure_openai_config
from packages.shared.config import Settings


# Creates an Azure OpenAI SDK client from validated settings.
def create_azure_openai_client(settings: Settings | None = None):
    config = get_azure_openai_config(settings)

    try:
        from openai import AzureOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "Azure OpenAI support requires the openai package. "
            "Install it with: pip install openai"
        ) from exc

    return AzureOpenAI(
        api_key=config.api_key,
        azure_endpoint=config.endpoint,
        api_version=config.api_version,
    )


# Returns the Azure OpenAI deployment name used for model calls.
def get_default_azure_deployment(settings: Settings | None = None) -> str:
    return get_azure_openai_config(settings).deployment


__all__ = [
    "AzureOpenAIModelConfig",
    "create_azure_openai_client",
    "get_default_azure_deployment",
]
