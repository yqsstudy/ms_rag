"""Test LLM service request options and error boundaries."""

import pytest

from src.generation.llm_service import LLMService, LLMServiceError


class FakeProvider:
    def __init__(self):
        self.kwargs = None

    def generate(self, prompt, **kwargs):
        self.kwargs = kwargs
        return "answer"

    def generate_stream(self, prompt, **kwargs):
        self.kwargs = kwargs
        yield "chunk"


class FailingProvider:
    def generate(self, prompt, **kwargs):
        raise RuntimeError("provider failure")

    def generate_stream(self, prompt, **kwargs):
        raise RuntimeError("provider failure")
        yield "unreachable"


def make_service(provider):
    service = LLMService.__new__(LLMService)
    service.provider_name = "fake"
    service.max_tokens = 123
    service.temperature = 0.2
    service.timeout = 45
    service.provider = provider
    return service


def test_generate_applies_configured_request_options():
    provider = FakeProvider()
    service = make_service(provider)

    assert service.generate("prompt") == "answer"
    assert provider.kwargs["max_tokens"] == 123
    assert provider.kwargs["temperature"] == 0.2
    assert provider.kwargs["timeout"] == 45


def test_generate_stream_applies_configured_request_options():
    provider = FakeProvider()
    service = make_service(provider)

    assert list(service.generate_stream("prompt")) == ["chunk"]
    assert provider.kwargs["max_tokens"] == 123
    assert provider.kwargs["temperature"] == 0.2
    assert provider.kwargs["timeout"] == 45


def test_generate_wraps_provider_errors():
    service = make_service(FailingProvider())

    with pytest.raises(LLMServiceError, match="LLM generation failed"):
        service.generate("prompt")


def test_generate_stream_wraps_provider_errors():
    service = make_service(FailingProvider())

    with pytest.raises(LLMServiceError, match="LLM stream generation failed"):
        list(service.generate_stream("prompt"))
