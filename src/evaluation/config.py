"""Configuration for offline RAG evaluation dataset generation."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field


_ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^{}]*|\$\{[^{}]+\}))?\}")


def _expand_env_string(value: str) -> str:
    previous = None
    expanded = value
    while previous != expanded:
        previous = expanded

        def replace(match: re.Match[str]) -> str:
            name = match.group(1)
            default = match.group(2) or ""
            return os.getenv(name) or _expand_env_string(default)

        expanded = _ENV_PATTERN.sub(replace, expanded)
    return expanded


def _expand_env(value: Any) -> Any:
    if isinstance(value, str):
        return _expand_env_string(value)
    if isinstance(value, list):
        return [_expand_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _expand_env(item) for key, item in value.items()}
    return value


class PathsConfig(BaseModel):
    corpus_dir: str = "./corpus"
    output_dir: str = "./data/eval"
    system_config: str = "./config/system.yaml"
    raw_response_dir: str = "./data/eval/raw_llm"


class LLMConfig(BaseModel):
    provider: str = "openai_compatible"
    base_url: str = ""
    api_key: str = Field(default="", repr=False)
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 4096
    timeout_seconds: int = 60
    max_retries: int = 3
    retry_backoff_seconds: float = 2.0
    save_raw_response: bool = True


class QuestionGenerationConfig(BaseModel):
    enabled_scopes: list[str] = Field(default_factory=lambda: ["chunk"])
    questions_per_chunk: int = 2
    chunk_questions_per_item: int | None = None
    section_questions_per_item: int = 1
    document_questions_per_item: int = 1
    max_chunks: int = 200
    max_sections: int = 50
    max_documents: int = 30
    min_chunk_chars: int = 200
    min_section_chars: int = 600
    min_document_chars: int = 1200
    allowed_types: list[str] = Field(default_factory=list)

    @property
    def chunk_question_count(self) -> int:
        return self.chunk_questions_per_item or self.questions_per_chunk


class CandidatePoolConfig(BaseModel):
    neighbor_window: int = 2
    same_section_limit: int = 8
    bm25_top_k: int = 50
    vector_top_k: int = 50
    title_match_top_k: int = 10


class CardFilterConfig(BaseModel):
    max_cards_per_question: int = 30
    snippet_chars: int = 240
    max_chunks_per_source: int = 5
    bm25_weight: float = 0.35
    vector_weight: float = 0.35
    title_match_bonus: float = 0.1
    same_doc_bonus: float = 0.1
    seed_neighbor_bonus: float = 0.1


class LLMJudgeConfig(BaseModel):
    relevance_threshold: int = 2
    batch_size: int = 20
    cards_per_request: int = 10


class SynthesisConfig(BaseModel):
    max_supporting_chunks: int = 8
    max_chunk_chars: int = 1200
    max_must_have_points: int = 5
    max_nice_to_have_points: int = 5


class ReviewConfig(BaseModel):
    sample_size: int = 50
    random_seed: int = 42
    stratify_by: list[str] = Field(default_factory=list)


class EvaluationConfig(BaseModel):
    dataset_path: str = "./data/eval/eval_dataset.jsonl"
    top_k: list[int] = Field(default_factory=lambda: [1, 3, 5, 10])
    run_generation: bool = False
    run_llm_judge: bool = False
    compare_configs: list[str] = Field(default_factory=list)
    fail_under: dict[str, float] = Field(default_factory=dict)


class RagEvalConfig(BaseModel):
    paths: PathsConfig = Field(default_factory=PathsConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    question_generation: QuestionGenerationConfig = Field(default_factory=QuestionGenerationConfig)
    candidate_pool: CandidatePoolConfig = Field(default_factory=CandidatePoolConfig)
    card_filter: CardFilterConfig = Field(default_factory=CardFilterConfig)
    llm_judge: LLMJudgeConfig = Field(default_factory=LLMJudgeConfig)
    synthesis: SynthesisConfig = Field(default_factory=SynthesisConfig)
    review: ReviewConfig = Field(default_factory=ReviewConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)

    @property
    def output_dir(self) -> Path:
        return Path(self.paths.output_dir)


def load_eval_config(path: str = "config/rag_eval.yaml") -> RagEvalConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"RAG eval config not found: {config_path}")

    project_root = config_path.resolve().parent.parent
    load_dotenv(project_root / ".env", override=False)
    load_dotenv(project_root / ".env.local", override=False)

    with config_path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}

    return RagEvalConfig.model_validate(_expand_env(raw))
