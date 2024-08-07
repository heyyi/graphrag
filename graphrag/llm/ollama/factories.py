# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""Factory functions for creating Ollama LLMs."""

import asyncio

from graphrag.llm.base import CachingLLM, RateLimitingLLM
from graphrag.llm.limiting import LLMLimiter
from graphrag.llm.types import (
    LLM,
    CompletionLLM,
    EmbeddingLLM,
    ErrorHandlerFn,
    LLMCache,
    LLMInvocationFn,
    OnCacheActionFn,
)

from .json_parsing_llm import JsonParsingLLM
from .ollama_chat_llm import OllamaChatLLM
from .ollama_embeddings_llm import OllamaEmbeddingsLLM
from .ollama_configuration import OllamaConfiguration
from .ollama_history_tracking_llm import OllamaHistoryTrackingLLM
from .ollama_token_relacing_llm import OllamaTokenReplacingLLM
from .types import OllamaClientTypes
from .utils import (
    RATE_LIMIT_ERRORS,
    RETRYABLE_ERRORS,
    get_completion_cache_args,
    get_sleep_time_from_error,
    get_token_counter,
)


def create_ollama_chat_llm(
    client: OllamaClientTypes,
    config: OllamaConfiguration,
    cache: LLMCache | None = None,
    limiter: LLMLimiter | None = None,
    semaphore: asyncio.Semaphore | None = None,
    on_invoke: LLMInvocationFn | None = None,
    on_error: ErrorHandlerFn | None = None,
    on_cache_hit: OnCacheActionFn | None = None,
    on_cache_miss: OnCacheActionFn | None = None,
) -> CompletionLLM:
    """Create an Ollama chat LLM."""
    operation = "chat"
    result = OllamaChatLLM(client, config)
    result.on_error(on_error)
    if limiter is not None or semaphore is not None:
        result = _rate_limited(result, config, operation, limiter, semaphore, on_invoke)
    if cache is not None:
        result = _cached(result, config, operation, cache, on_cache_hit, on_cache_miss)
    result = OllamaHistoryTrackingLLM(result)
    result = OllamaTokenReplacingLLM(result)
    return JsonParsingLLM(result)


def create_ollama_embedding_llm(
    client: OllamaClientTypes,
    config: OllamaConfiguration,
    cache: LLMCache | None = None,
    limiter: LLMLimiter | None = None, 
    semaphore: asyncio.Semaphore | None = None,
    on_invoke: LLMInvocationFn | None = None,
    on_error: ErrorHandlerFn | None = None,
    on_cache_hit: OnCacheActionFn | None = None,
    on_cache_miss: OnCacheActionFn | None = None,
) -> EmbeddingLLM:
    """Create an Ollama embedding LLM."""
    operation = "embedding"
    result = OllamaEmbeddingsLLM(client, config)
    result.on_error(on_error)
    if limiter is not None or semaphore is not None:
        result = _rate_limited(result, config, operation, limiter, semaphore, on_invoke)
    if cache is not None:
        result = _cached(result, config, operation, cache, on_cache_hit, on_cache_miss)
    return result
    
    

def _rate_limited(
    delegate: LLM,
    config: OllamaConfiguration,
    operation: str,
    limiter: LLMLimiter | None,
    semaphore: asyncio.Semaphore | None,
    on_invoke: LLMInvocationFn | None,
):
    result = RateLimitingLLM(
        delegate,
        config,
        operation,
        RETRYABLE_ERRORS,
        RATE_LIMIT_ERRORS,
        limiter,
        semaphore,
        get_token_counter(config),
        get_sleep_time_from_error,
    )
    result.on_invoke(on_invoke)
    return result
    

def _cached(
    delegate: LLM,
    config: OllamaConfiguration,
    operation: str,
    cache: LLMCache,
    on_cache_hit: OnCacheActionFn | None,
    on_cache_miss: OnCacheActionFn | None,
):
    cache_args = get_completion_cache_args(config)
    result = CachingLLM(delegate, cache_args, operation, cache)
    result.on_cache_hit(on_cache_hit)
    result.on_cache_miss(on_cache_miss)
    return result