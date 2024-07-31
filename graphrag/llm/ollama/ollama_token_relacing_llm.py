# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""The Chat-based language model."""

from typing_extensions import Unpack

from graphrag.llm.types import (
    LLM,
    CompletionInput,
    CompletionLLM,
    CompletionOutput,
    LLMInput,
    LLMOutput,
)

from .utils import perform_variable_replacements


class OllamaTokenReplacingLLM(LLM[CompletionInput, CompletionOutput]):
    """An Ollama History-Tracking LLM."""
    
    _delegate: CompletionLLM
    
    def __init__(self, delegate: CompletionLLM):
        self._delegate = delegate
        
    async def __call__(
        self,
        input: CompletionInput,
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[CompletionOutput]:
        """Call the LLM with the input and kwargs."""
        variables = kwargs.get("variables")
        history = kwargs.get("history") or []
        input = perform_variable_replacements(input, history, variables)
        return await self._delegate(input, **kwargs)