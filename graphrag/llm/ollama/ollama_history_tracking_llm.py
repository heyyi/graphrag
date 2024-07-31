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


class OllamaHistoryTrackingLLM(LLM[CompletionInput, CompletionOutput]):
    """An Ollama History-Tracking LLM."""
    
    _delegate: CompletionLLM
    
    def __init__(self, delegate: CompletionLLM):
        self._delegate = delegate
        
    async def __call__(
        self,
        input: CompletionInput,
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[CompletionOutput]:
        """Call the LLM."""
        history = kwargs.get("history") or []
        output = await self._delegate(input, **kwargs)
        return LLMOutput(
            output=output.output,
            json=output.json,
            history=[*history, {"role": "system", "content": output.output}],
        )