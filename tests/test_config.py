"""Test configuration loading."""

from src.core.config import Settings


def test_yaml_env_substitution_is_recursive(tmp_path, monkeypatch):
    monkeypatch.setenv("MS_RAG_ADMIN_TOKEN", "admin-secret")
    config_path = tmp_path / "system.yaml"
    config_path.write_text(
        """
api:
  admin_token: "${MS_RAG_ADMIN_TOKEN:}"
llm:
  provider: "${LLM_PROVIDER:anthropic}"
  api_key: "${MS_RAG_TEST_LLM_API_KEY:test-key}"
""".strip(),
        encoding="utf-8",
    )

    settings = Settings.from_yaml(str(config_path))

    assert settings.api.admin_token == "admin-secret"
    assert settings.llm.provider == "anthropic"
    assert settings.llm.api_key == "test-key"
