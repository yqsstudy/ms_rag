"""LLM service with multi-provider support"""

from abc import ABC, abstractmethod
from typing import Iterator, Optional

from anthropic import Anthropic
from openai import OpenAI


class LLMProvider(ABC):
    """Abstract LLM provider"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response synchronously"""
        pass

    @abstractmethod
    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """Generate response as stream"""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2000)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        max_tokens = kwargs.get("max_tokens", 2000)
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text


class OpenAIProvider(LLMProvider):
    """OpenAI provider"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2000)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        max_tokens = kwargs.get("max_tokens", 2000)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class DeepSeekProvider(LLMProvider):
    """DeepSeek provider"""

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
        )
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2000)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        max_tokens = kwargs.get("max_tokens", 2000)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class LLMService:
    """LLM service with multi-provider support"""

    PROVIDERS = {
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
    }

    def __init__(
        self,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ):
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. "
                           f"Available: {list(self.PROVIDERS.keys())}")

        self.provider_name = provider
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Use default model for provider if not specified
        if model is None:
            model = self._get_default_model(provider)

        self.provider = self.PROVIDERS[provider](api_key, model)

    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider"""
        defaults = {
            "anthropic": "claude-sonnet-4-6",
            "openai": "gpt-4-turbo",
            "deepseek": "deepseek-chat",
        }
        return defaults.get(provider, "")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response"""
        kwargs.setdefault("max_tokens", self.max_tokens)
        kwargs.setdefault("temperature", self.temperature)
        return self.provider.generate(prompt, **kwargs)

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """Generate response as stream"""
        kwargs.setdefault("max_tokens", self.max_tokens)
        kwargs.setdefault("temperature", self.temperature)
        return self.provider.generate_stream(prompt, **kwargs)