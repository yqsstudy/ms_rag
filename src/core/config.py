"""Configuration management using Pydantic"""

import os
from pathlib import Path
from typing import Literal, Optional

import yaml
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file
load_dotenv()


class EmbeddingConfig(BaseSettings):
    """Embedding configuration"""

    model: str = "BAAI/bge-large-zh"
    device: Literal["cpu", "cuda", "mps"] = "cpu"
    batch_size: int = 32
    normalize: bool = True


class VectorStoreConfig(BaseSettings):
    """Vector store configuration"""

    type: Literal["chroma", "milvus"] = "chroma"
    persist_directory: str = "./data/chroma"
    collection_name: str = "performance_guide"


class KeywordIndexConfig(BaseSettings):
    """Keyword index configuration"""

    type: Literal["bm25"] = "bm25"
    k1: float = 1.5  # BM25 term frequency saturation parameter
    b: float = 0.75  # BM25 length normalization parameter


class RetrievalConfig(BaseSettings):
    """Retrieval configuration"""

    vector_weight: float = Field(default=0.6, ge=0.0, le=1.0)
    keyword_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    top_k: int = Field(default=10, ge=1, le=50)
    rerank: bool = True
    reranker_mode: Literal["heuristic", "cross_encoder"] = "heuristic"
    reranker_model: str = "BAAI/bge-reranker-base"
    reranker_fallback: Literal["heuristic", "none"] = "heuristic"


class LLMConfig(BaseSettings):
    """LLM configuration"""

    provider: Literal["anthropic", "openai", "deepseek"] = "anthropic"
    model: str = "claude-sonnet-4-6"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    max_tokens: int = Field(default=2000, ge=100, le=8000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    timeout: int = Field(default=60, ge=10, le=300)


class APIConfig(BaseSettings):
    """API configuration"""

    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    debug: bool = False
    cors_origins: list[str] = ["*"]
    admin_token: Optional[str] = None


class DocumentConfig(BaseSettings):
    """Document processing configuration"""

    min_chunk_size: int = Field(default=1500, ge=100)
    max_chunk_size: int = Field(default=2000, ge=500)
    chunk_overlap: int = Field(default=200, ge=0)
    child_chunk_size: int = Field(default=400, ge=50)
    child_chunk_overlap: int = Field(default=50, ge=0)


class LoggingConfig(BaseSettings):
    """Logging configuration"""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    format: Literal["standard", "json"] = "json"
    file: str = "./logs/app.log"


class CacheConfig(BaseSettings):
    """Cache configuration"""

    enabled: bool = True

    # L1: exact match cache
    l1_max_size: int = Field(default=1000, ge=10)
    l1_ttl: int = Field(default=3600, ge=60)

    # L2: semantic similarity cache
    l2_max_size: int = Field(default=500, ge=10)
    l2_ttl: int = Field(default=1800, ge=60)
    l2_threshold: float = Field(default=0.92, ge=0.5, le=1.0)

    # L3: embedding cache
    l3_max_size: int = Field(default=2000, ge=10)
    l3_ttl: int = Field(default=7200, ge=60)


class KnowledgeGraphConfig(BaseSettings):
    """Knowledge graph enhancement configuration"""

    enabled: bool = True
    graph_path: str = "./data/graph.json"
    expand_parent: bool = True
    expand_sibling: bool = True
    expand_child: bool = True
    expand_reference: bool = True
    max_expand_per_direction: int = Field(default=1, ge=1, le=5)
    max_enhanced_results: int = Field(default=3, ge=1, le=10)
    expand_weight_parent: float = Field(default=0.5, ge=0.0, le=1.0)
    expand_weight_sibling: float = Field(default=0.3, ge=0.0, le=1.0)
    expand_weight_child: float = Field(default=0.3, ge=0.0, le=1.0)
    expand_weight_reference: float = Field(default=0.4, ge=0.0, le=1.0)
    related_topics_count: int = Field(default=5, ge=1, le=10)


class Settings(BaseSettings):
    """Main settings class"""

    model_config = SettingsConfigDict(
        env_prefix="MS_RAG_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    embedding: EmbeddingConfig = EmbeddingConfig()
    vector_store: VectorStoreConfig = VectorStoreConfig()
    keyword_index: KeywordIndexConfig = KeywordIndexConfig()
    retrieval: RetrievalConfig = RetrievalConfig()
    llm: LLMConfig = LLMConfig()
    api: APIConfig = APIConfig()
    document: DocumentConfig = DocumentConfig()
    logging: LoggingConfig = LoggingConfig()
    cache: CacheConfig = CacheConfig()
    knowledge_graph: KnowledgeGraphConfig = KnowledgeGraphConfig()

    # Paths
    corpus_path: str = "./corpus"
    config_path: str = "./config"

    @classmethod
    def _resolve_env_var(cls, value: str) -> Optional[str]:
        """Resolve ${VAR} or ${VAR:default} syntax"""
        if not (value.startswith("${") and value.endswith("}")):
            return value
        inner = value[2:-1]
        if ":" in inner:
            env_var, default = inner.split(":", 1)
        else:
            env_var, default = inner, None
        return os.environ.get(env_var, default)

    @classmethod
    def _resolve_env_vars(cls, value):
        if isinstance(value, dict):
            return {key: cls._resolve_env_vars(item) for key, item in value.items()}
        if isinstance(value, list):
            return [cls._resolve_env_vars(item) for item in value]
        if isinstance(value, str):
            return cls._resolve_env_var(value)
        return value

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "Settings":
        """Load settings from YAML file"""
        with open(yaml_path, encoding="utf-8") as f:
            config_dict = yaml.safe_load(f)

        return cls(**cls._resolve_env_vars(config_dict))

    def get_llm_api_key(self) -> str:
        """Get LLM API key from config or environment"""
        if self.llm.api_key:
            return self.llm.api_key

        # Try provider-specific environment variable
        env_key = f"{self.llm.provider.upper()}_API_KEY"
        api_key = os.environ.get(env_key)

        if not api_key:
            api_key = os.environ.get("LLM_API_KEY")

        if not api_key:
            raise ValueError(
                f"LLM API key not found. Set {env_key} or LLM_API_KEY environment variable"
            )

        return api_key


def get_settings(config_path: Optional[str] = None) -> Settings:
    """Get settings instance"""
    if config_path is None:
        config_path = os.environ.get("MS_RAG_CONFIG_PATH", "./config/system.yaml")

    if Path(config_path).exists():
        return Settings.from_yaml(config_path)

    return Settings()