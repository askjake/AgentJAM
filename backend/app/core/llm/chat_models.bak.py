from functools import cache
import os

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_aws import ChatBedrockConverse

from app.core.llm.coverity_assist_chat_model import CoverityAssistChatModel

# Optional providers
try:
    from langchain_community.chat_models import ChatOllama  # type: ignore
except Exception:
    try:
        from langchain_community.chat_models.ollama import ChatOllama  # type: ignore
    except Exception:
        ChatOllama = None  # type: ignore

try:
    from langchain_openai import ChatOpenAI  # type: ignore
except Exception:
    ChatOpenAI = None  # type: ignore

from app.config import get_settings

settings = get_settings()


def _infer_bedrock_provider(model_id: str | None) -> str | None:
    if not model_id:
        return None

    lowered = model_id.lower()
    if "anthropic" in lowered:
        return "anthropic"
    if "amazon" in lowered:
        return "amazon"
    if "meta" in lowered:
        return "meta"
    if "mistral" in lowered:
        return "mistral"
    if "cohere" in lowered:
        return "cohere"
    if "application-inference-profile/" in lowered or "inference-profile/" in lowered:
        return (
            os.getenv("BEDROCK_APPLICATION_INFERENCE_PROFILE_PROVIDER")
            or os.getenv("BEDROCK_INFERENCE_PROFILE_PROVIDER")
            or "anthropic"
        )
    return None


def _build_bedrock_model(model_id: str, max_tokens: int) -> ChatBedrockConverse:
    kwargs = {
        "model": model_id,
        "max_tokens": max_tokens,
        "region_name": settings.AWS_REGION,
        "disable_streaming": os.getenv("DISABLE_STREAMING","0").lower() in ("1","true","yes","y"),
    }

    if isinstance(model_id, str) and model_id.startswith("arn:"):
        provider = _infer_bedrock_provider(model_id)
        if provider:
            kwargs["provider"] = provider

    return ChatBedrockConverse(**kwargs)


def _build_coverity_assist_model(max_tokens: int) -> CoverityAssistChatModel:
    token = os.getenv("COVERITY_ASSIST_TOKEN") or settings.COVERITY_ASSIST_TOKEN or ""
    if not token:
        raise RuntimeError("COVERITY_ASSIST_TOKEN is required for coverity-assist provider")

    endpoint_url = os.getenv("COVERITY_ASSIST_URL") or settings.COVERITY_ASSIST_URL
    inference_profile_arn = (
        os.getenv("COVERITY_ASSIST_INFERENCE_PROFILE_ARN")
        or settings.COVERITY_ASSIST_INFERENCE_PROFILE_ARN
        or None
    )
    gateway_cap = int(os.getenv("COVERITY_ASSIST_MAX_TOKENS", str(settings.COVERITY_ASSIST_MAX_TOKENS)))
    effective_max_tokens = min(max_tokens, gateway_cap)

    return CoverityAssistChatModel(
        endpoint_url=endpoint_url,
        bearer_token=token,
        max_tokens=effective_max_tokens,
        verify_ssl=bool(os.getenv("COVERITY_ASSIST_VERIFY_SSL", str(int(settings.COVERITY_ASSIST_VERIFY_SSL))).lower() not in ("0", "false", "no", "off")),
        use_top_level_system=bool(os.getenv("COVERITY_ASSIST_TOP_LEVEL_SYSTEM", str(int(settings.COVERITY_ASSIST_TOP_LEVEL_SYSTEM))).lower() not in ("0", "false", "no", "off")),
        inference_profile_arn=inference_profile_arn,
        include_system_prompt=False,
    )


def _build_ollama_model(model_id: str, max_tokens: int, api_base: str | None) -> BaseChatModel:
    if ChatOllama is None:
        raise RuntimeError("langchain-community is not installed; cannot use ollama provider")
    base_url = api_base or os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434"
    return ChatOllama(model=model_id, base_url=base_url, num_predict=max_tokens)


def _build_openai_like_model(model_id: str, max_tokens: int, api_base: str | None) -> BaseChatModel:
    if ChatOpenAI is None:
        raise RuntimeError("langchain-openai is not installed; cannot use openai provider")
    base_url = api_base or os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
    api_key = os.getenv("OPENAI_API_KEY", "ollama")

    kwargs: dict = {"model": model_id, "api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
        kwargs["openai_api_base"] = base_url

    kwargs["max_tokens"] = max_tokens
    kwargs["max_completion_tokens"] = max_tokens

    return ChatOpenAI(**kwargs)


@cache
def get_model(efficient: bool = False) -> BaseChatModel:
    """Return the configured chat model."""

    if efficient and settings.ELLM_MODEL:
        if settings.ELLM_PROVIDER == "coverity-assist":
            return _build_coverity_assist_model(max_tokens=4096)
        if settings.ELLM_PROVIDER == "aws-bedrock":
            return _build_bedrock_model(model_id=settings.ELLM_MODEL, max_tokens=4096)
        if settings.ELLM_PROVIDER == "ollama":
            return _build_ollama_model(model_id=settings.ELLM_MODEL, max_tokens=4096, api_base=settings.ELLM_API_BASE)
        if settings.ELLM_PROVIDER in ("openai", "anthropic"):
            return _build_openai_like_model(model_id=settings.ELLM_MODEL, max_tokens=4096, api_base=settings.ELLM_API_BASE)
        raise NotImplementedError(f"Provider {settings.ELLM_PROVIDER} not implemented yet")

    if settings.PLLM_PROVIDER == "coverity-assist":
        return _build_coverity_assist_model(max_tokens=settings.MAX_OUTPUT_COUNT)
    if settings.PLLM_PROVIDER == "aws-bedrock":
        return _build_bedrock_model(model_id=settings.PLLM_MODEL, max_tokens=settings.MAX_OUTPUT_COUNT)
    if settings.PLLM_PROVIDER == "ollama":
        return _build_ollama_model(model_id=settings.PLLM_MODEL, max_tokens=settings.MAX_OUTPUT_COUNT, api_base=settings.PLLM_API_BASE)
    if settings.PLLM_PROVIDER in ("openai", "anthropic"):
        return _build_openai_like_model(model_id=settings.PLLM_MODEL, max_tokens=settings.MAX_OUTPUT_COUNT, api_base=settings.PLLM_API_BASE)

    raise NotImplementedError(f"Provider {settings.PLLM_PROVIDER} not implemented yet")
