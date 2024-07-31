# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""Utility functions for the Ollama API."""

import json
import logging
from collections.abc import Callable
from typing import Any

import tiktoken
from openai import (
    APIConnectionError,
    InternalServerError,
    RateLimitError,
)

from .ollama_configuration import OllamaConfiguration

DEFAULT_ENCODING = "cl100k_base"

_encoders: dict[str, tiktoken.Encoding] = {}

RETRYABLE_ERRORS: list[type[Exception]] = [
    RateLimitError,
    APIConnectionError,
    InternalServerError,
]
RATE_LIMIT_ERRORS: list[type[Exception]] = [RateLimitError]

log = logging.getLogger(__name__)


def get_token_counter(config: OllamaConfiguration) -> Callable[[str], int]:
    """Get a function that counts the number of tokens in a string."""
    model = config.encoding_model or "cl100k_base"
    enc = _encoders.get(model)
    if enc is None:
        enc = tiktoken.get_encoding(model)
        _encoders[model] = enc
        
    return lambda s: len(enc.encode(s))


def get_completion_cache_args(configuration: OllamaConfiguration) -> dict:
    """Get the cache arguments for a completion LLM."""
    return {
        "model": configuration.model,
        "temperature": configuration.temperature,
        "top_p": configuration.top_p,
        "max_tokens": configuration.max_tokens,
    }

def get_completion_llm_args(
    parameters: dict | None, configuration: OllamaConfiguration
) -> dict:
    """Get the arguments for a completion LLM."""
    return {
        **get_completion_cache_args(configuration),
        **(parameters or {})
    }

def try_parse_json_object(input: str) -> dict:
    """Generate JSON-string output using best-attempt prompting & parsing techniques."""
    try:
        result = json.loads(input)
    except json.JSONDecodeError:
        log.exception("error loading json, json=%s", input)
        raise
    else:
        if not isinstance(result, dict):
            raise TypeError
        return result
    

def perform_variable_replacements(
    input: str, history: list[dict], variables: dict | None
) -> str:
    """Perform variable replacements on the input string and in a chat log."""
    result = input
    
    def replace_all(input: str) -> str:
        result = input
        if variables:
            for entry in variables:
                result = result.replace(f"{{{entry}}}", variables[entry])
        return result
    for i in range(len(history)):
        entry = history[i]
        if entry.get("role") == "system":
            history[i]["content"] = replace_all(entry.get("content") or "")
            
    return result
    
    
def get_sleep_time_from_error(e: Any) -> float:
    """Extract the sleep time value from a RateLimitError. This is usually only available in Azure."""
    sleep_time = 0.0
    if isinstance(e, RateLimitError) and _please_retry_after in str(e):
        sleep_time = int(str(e).split(_please_retry_after)[1].split(" second")[0])
        
    return sleep_time

_please_retry_after = "Please retry after "


