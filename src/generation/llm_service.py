"""LLM service with multi-provider support"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Iterator, Optional

from anthropic import Anthropic
from openai import OpenAI

logger = logging.getLogger("ms_rag")


class LLMServiceError(RuntimeError):
    pass


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

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6", base_url: str = None):
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = Anthropic(**kwargs)
        self.model = model
        logger.info(f"[Anthropic] Initialized with model={model}, base_url={base_url}")

    def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2000)
        temperature = kwargs.get("temperature", 0.7)
        timeout = kwargs.get("timeout")
        logger.info("[Anthropic] generate called, model=%s, max_tokens=%s", self.model, max_tokens)
        t0 = time.time()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
            messages=[{"role": "user", "content": prompt}],
        )
        logger.info("[Anthropic] generate done in %.2fs", time.time() - t0)
        return response.content[0].text

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        max_tokens = kwargs.get("max_tokens", 2000)
        temperature = kwargs.get("temperature", 0.7)
        timeout = kwargs.get("timeout")
        logger.info("[Anthropic] generate_stream called, model=%s, max_tokens=%s", self.model, max_tokens)
        t0 = time.time()
        chunk_count = 0
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            logger.info("[Anthropic] Stream opened in %.2fs", time.time() - t0)
            for text in stream.text_stream:
                chunk_count += 1
                yield text
        logger.info("[Anthropic] Stream finished, %s chunks in %.2fs", chunk_count, time.time() - t0)


class OpenAIProvider(LLMProvider):
    """OpenAI provider"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo", base_url: str = None):
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = model
        logger.info(f"[OpenAI] Initialized with model={model}, base_url={base_url}")

    def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2000)
        logger.info(f"[OpenAI] generate called, model={self.model}")
        t0 = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=kwargs.get("temperature", 0.7),
            timeout=kwargs.get("timeout"),
        )
        logger.info(f"[OpenAI] generate done in {time.time()-t0:.2f}s")
        return response.choices[0].message.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        max_tokens = kwargs.get("max_tokens", 2000)
        logger.info(f"[OpenAI] generate_stream called, model={self.model}")
        t0 = time.time()
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=kwargs.get("temperature", 0.7),
            timeout=kwargs.get("timeout"),
            stream=True,
        )
        chunk_count = 0
        for chunk in stream:
            if chunk.choices[0].delta.content:
                chunk_count += 1
                yield chunk.choices[0].delta.content
        logger.info(f"[OpenAI] Stream finished, {chunk_count} chunks in {time.time()-t0:.2f}s")


class DeepSeekProvider(LLMProvider):
    """DeepSeek provider"""

    def __init__(self, api_key: str, model: str = "deepseek-chat", base_url: str = None):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url or "https://api.deepseek.com/v1",
        )
        self.model = model
        logger.info(f"[DeepSeek] Initialized with model={model}, base_url={base_url or 'https://api.deepseek.com/v1'}")

    def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2000)
        logger.info(f"[DeepSeek] generate called, model={self.model}")
        t0 = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=kwargs.get("temperature", 0.7),
            timeout=kwargs.get("timeout"),
        )
        logger.info(f"[DeepSeek] generate done in {time.time()-t0:.2f}s")
        return response.choices[0].message.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        max_tokens = kwargs.get("max_tokens", 2000)
        logger.info(f"[DeepSeek] generate_stream called, model={self.model}")
        t0 = time.time()
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=kwargs.get("temperature", 0.7),
            timeout=kwargs.get("timeout"),
            stream=True,
        )
        chunk_count = 0
        for chunk in stream:
            if chunk.choices[0].delta.content:
                chunk_count += 1
                yield chunk.choices[0].delta.content
        logger.info(f"[DeepSeek] Stream finished, {chunk_count} chunks in {time.time()-t0:.2f}s")


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
        base_url: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. "
                           f"Available: {list(self.PROVIDERS.keys())}")

        self.provider_name = provider
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        # Use default model for provider if not specified
        if model is None:
            model = self._get_default_model(provider)

        self.provider = self.PROVIDERS[provider](api_key, model, base_url)

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
        kwargs.setdefault("timeout", self.timeout)
        logger.info("[LLM] generate via %s", self.provider_name)
        try:
            return self.provider.generate(prompt, **kwargs)
        except Exception as exc:
            logger.exception("[LLM] generate failed via %s", self.provider_name)
            raise LLMServiceError("LLM generation failed") from exc

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """Generate response as stream"""
        kwargs.setdefault("max_tokens", self.max_tokens)
        kwargs.setdefault("temperature", self.temperature)
        kwargs.setdefault("timeout", self.timeout)
        logger.info("[LLM] generate_stream via %s", self.provider_name)
        try:
            yield from self.provider.generate_stream(prompt, **kwargs)
        except Exception as exc:
            logger.exception("[LLM] stream generation failed via %s", self.provider_name)
            raise LLMServiceError("LLM stream generation failed") from exc