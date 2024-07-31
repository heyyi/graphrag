# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""A base class for Ollama-based LLMs."""

from ollama import (
    AsyncClient,
)

OllamaClientTypes = AsyncClient