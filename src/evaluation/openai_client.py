"""OpenAI-compatible client for offline evaluation jobs."""

from __future__ import annotations

import json
import time
from typing import Any

import httpx


def extract_json_object(text: str) -> Any:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    start_candidates = [pos for pos in [stripped.find("{"), stripped.find("[")] if pos != -1]
    if not start_candidates:
        raise ValueError("No JSON object or array found in LLM response")
    start = min(start_candidates)
    end = max(stripped.rfind("}"), stripped.rfind("]"))
    if end <= start:
        raise ValueError("Incomplete JSON object or array in LLM response")
    return json.loads(stripped[start:end + 1])


class OpenAICompatibleClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_seconds: int = 60,
        max_retries: int = 3,
        retry_backoff_seconds: float = 2.0,
    ):
        if not base_url:
            raise ValueError("OpenAI-compatible base_url is required")
        if not api_key:
            raise ValueError("OpenAI-compatible api_key is required")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds

    def chat_text(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout_seconds) as client:
                    response = client.post(url, headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt >= self.max_retries:
                    break
                time.sleep(self.retry_backoff_seconds * (2 ** attempt))
        raise RuntimeError(f"LLM request failed after retries: {last_error}")

    def chat_json(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> tuple[Any, str]:
        text = self.chat_text(messages, temperature=temperature, max_tokens=max_tokens)
        return extract_json_object(text), text
