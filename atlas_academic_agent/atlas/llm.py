"""
LLM configuration and client for NVIDIA NeMo models.
"""

from typing import List, Dict, Optional
from openai import AsyncOpenAI


class LLMConfig:
    """Configuration settings for the LLM."""
    base_url: str = "https://integrate.api.nvidia.com/v1"
    model: str = "nvidia/nemotron-4-340b-instruct"
    max_tokens: int = 1024
    default_temp: float = 0.5


class NeMoLLaMa:
    """
    A class to interact with NVIDIA's nemotron-4-340b-instruct model through their API.
    This implementation uses AsyncOpenAI client for asynchronous operations.

    Key Differences from synchronous OpenAI:
        - AsyncOpenAI: Asynchronous operations using async/await
        - Use Cases: High throughput, non-blocking operations

    Attributes:
        config: LLM configuration settings
        client: AsyncOpenAI client instance
        _is_authenticated: Authentication status flag
    """

    def __init__(self, api_key: str):
        """
        Initialize NeMoLLaMa with API key.

        Args:
            api_key: NVIDIA API authentication key
        """
        self.config = LLMConfig()
        self.client = AsyncOpenAI(
            base_url=self.config.base_url,
            api_key=api_key
        )
        self._is_authenticated = False

    async def check_auth(self) -> bool:
        """
        Verify API authentication with test request.

        Returns:
            Authentication status

        Example:
            >>> is_valid = await llm.check_auth()
            >>> print(f"Authenticated: {is_valid}")
        """
        test_message = [{"role": "user", "content": "test"}]
        try:
            await self.agenerate(test_message, temperature=0.1)
            self._is_authenticated = True
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return False

    async def agenerate(
        self,
        messages: List[Dict],
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate text using NeMo LLaMa model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0, default from config)

        Returns:
            Generated text response

        Example:
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant"},
            ...     {"role": "user", "content": "Plan my study schedule"}
            ... ]
            >>> response = await llm.agenerate(messages, temperature=0.7)
        """
        completion = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temperature or self.config.default_temp,
            max_tokens=self.config.max_tokens,
            stream=False
        )
        return completion.choices[0].message.content
