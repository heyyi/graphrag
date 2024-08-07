# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""OpenAI wrapper options."""

from enum import Enum
from typing import Any, cast

import openai

OPENAI_RETRY_ERROR_TYPES = (
    # TODO: update these when we update to OpenAI 1+ library
    cast(Any, openai).RateLimitError,
    cast(Any, openai).APIConnectionError,
    # TODO: replace with comparable OpenAI 1+ error
)


class OllamaApiType(str, Enum):
    """The Ollama Flavor."""

    Ollama = "ollama"

