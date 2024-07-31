# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""Create Ollama client instance."""

import logging
from functools import cache

from ollama import AsyncClient

from .ollama_configuration import OllamaConfiguration
from .types import OllamaClientTypes

log = logging.getLogger(__name__)

API_BASE_REQUIRED_FOR_OLLAMA = "api_base is required for Ollama client"

@cache
def create_ollama_client(
    configuration: OllamaConfiguration
) -> OllamaClientTypes:
    """Create a new Ollama client instance."""
    api_base = configuration.api_base
    if api_base is None:
        raise ValueError(API_BASE_REQUIRED_FOR_OLLAMA)
    log.info("Creating async Ollama client base_url=%s", configuration.api_base)
    return AsyncClient(
        host=configuration.api_base,
        timeout=configuration.request_timeout or 180.0,
    )
    