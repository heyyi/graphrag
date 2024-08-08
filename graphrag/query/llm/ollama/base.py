# Copyright (c) 2024 DELL Corporation.
# Author yi.he@dell.com

"""Base classes for LLM and Embedding models."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, OpenAI
from ollama import Client, AsyncClient

from graphrag.query.llm.base import BaseTextEmbedding
from graphrag.query.llm.ollama.typing import OllamaApiType
from graphrag.query.progress import ConsoleStatusReporter, StatusReporter


class BaseOllamaLLM(ABC):
    """The Base OpenAI LLM implementation."""

    _async_client: AsyncClient
    _sync_client: Client

    def __init__(self):
        self._create_ollama_client()

    @abstractmethod
    def _create_ollama_client(self):
        """Create a new synchronous and asynchronous OpenAI client instance."""

    def set_clients(
        self,
        sync_client: Client,
        async_client: AsyncClient,
    ):
        """
        Set the synchronous and asynchronous clients used for making API requests.

        Args:
            sync_client (Client): The sync client object.
            async_client (AsyncClient): The async client object.
        """
        self._sync_client = sync_client
        self._async_client = async_client

    @property
    def async_client(self) -> AsyncClient | None:
        """
        Get the asynchronous client used for making API requests.

        Returns
        -------
            AsyncClient: The async client object.
        """
        return self._async_client

    @property
    def sync_client(self) -> Client | None:
        """
        Get the synchronous client used for making API requests.

        Returns
        -------
            Client: The async client object.
        """
        return self._sync_client

    @async_client.setter
    def async_client(self, client: AsyncClient):
        """
        Set the asynchronous client used for making API requests.

        Args:
            client (AsyncClient): The async client object.
        """
        self._async_client = client

    @sync_client.setter
    def sync_client(self, client: Client):
        """
        Set the synchronous client used for making API requests.

        Args:
            client (Client): The sync client object.
        """
        self._sync_client = client


class OllamaLLMImpl(BaseOllamaLLM):
    """Orchestration OpenAI LLM Implementation."""

    _reporter: StatusReporter = ConsoleStatusReporter()

    def __init__(
        self,
        api_key: str | None = None,
        azure_ad_token_provider: Callable | None = None,
        deployment_name: str | None = None,
        api_base: str | None = None,
        api_version: str | None = None,
        api_type: OllamaApiType = OllamaApiType.Ollama,
        organization: str | None = None,
        max_retries: int = 10,
        request_timeout: float = 180.0,
        reporter: StatusReporter | None = None,
    ):
        self.api_key = api_key
        self.azure_ad_token_provider = azure_ad_token_provider
        self.deployment_name = deployment_name
        self.api_base = api_base
        self.api_version = api_version
        self.api_type = api_type
        self.organization = organization
        self.max_retries = max_retries
        self.request_timeout = request_timeout
        self.reporter = reporter or ConsoleStatusReporter()

        try:
            # Create OpenAI sync and async clients
            super().__init__()
        except Exception as e:
            self._reporter.error(
                message="Failed to create Ollama client",
                details={self.__class__.__name__: str(e)},
            )
            raise

    def _create_ollama_client(self):
        """Create a new Ollama client instance."""
        sync_client = Client(
            host=self.api_base,
            timeout=self.request_timeout,
        )
        async_client = AsyncClient(
            host=self.api_base,
            timeout=self.request_timeout,
        )
        self.set_clients(sync_client=sync_client, async_client=async_client)


class OllamaTextEmbeddingImpl(BaseTextEmbedding):
    """Orchestration OpenAI Text Embedding Implementation."""

    _reporter: StatusReporter | None = None

    def _create_openai_client(self, api_type: OllamaApiType):
        """Create a new synchronous and asynchronous OpenAI client instance."""
