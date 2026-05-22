"""Pydantic schemas for RAG evaluation artifacts."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChunkRecord(BaseModel):
    chunk_id: str
    doc_id: str = ""
    source_file: str = ""
    doc_title: str = ""
    section_title: str = ""
    section_path: str = ""
    content: str
    parent_id: str = ""
    prev_chunk_id: str | None = None
    next_chunk_id: str | None = None


class GeneratedQuestion(BaseModel):
    id: str
    question: str
    seed_chunk_id: str
    seed_chunk_ids: list[str] = Field(default_factory=list)
    seed_source_file: str = ""
    question_scope: str = "chunk"
    doc_id: str = ""
    doc_title: str = ""
    section_title: str = ""
    section_path: str = ""
    question_type: str = "default"
    difficulty: str = "medium"
    keywords: list[str] = Field(default_factory=list)


class CandidateChunk(BaseModel):
    chunk_id: str
    source_file: str = ""
    origin: list[str] = Field(default_factory=list)
    bm25_score: float = 0.0
    vector_score: float = 0.0
    bm25_rank: int | None = None
    vector_rank: int | None = None
    title_match: bool = False
    same_doc: bool = False
    seed_neighbor: bool = False


class CandidatePool(BaseModel):
    question_id: str
    question: str
    seed_chunk_id: str
    candidate_chunks: list[CandidateChunk] = Field(default_factory=list)


class EvidenceCard(BaseModel):
    chunk_id: str
    source_file: str = ""
    doc_title: str = ""
    section_path: str = ""
    matched_keywords: list[str] = Field(default_factory=list)
    snippet: str = ""
    bm25_rank: int | None = None
    vector_rank: int | None = None
    score: float = 0.0


class EvidenceCardSet(BaseModel):
    question_id: str
    question: str
    seed_chunk_id: str
    cards: list[EvidenceCard] = Field(default_factory=list)


class JudgedChunk(BaseModel):
    chunk_id: str
    relevance: int = 0
    supported_points: list[str] = Field(default_factory=list)
    reason: str = ""


class EvidenceJudgment(BaseModel):
    question_id: str
    question: str
    judged_chunks: list[JudgedChunk] = Field(default_factory=list)


class AnswerKeyPoint(BaseModel):
    point: str
    supporting_chunks: list[str] = Field(default_factory=list)


class EvalSample(BaseModel):
    id: str
    question: str
    question_type: str = "default"
    difficulty: str = "medium"
    question_scope: str = "chunk"
    doc_id: str = ""
    doc_title: str = ""
    section_title: str = ""
    section_path: str = ""
    answer_key_points: list[AnswerKeyPoint] = Field(default_factory=list)
    must_have_points: list[str] = Field(default_factory=list)
    nice_to_have_points: list[str] = Field(default_factory=list)
    expected_answer: str = ""
    acceptable_chunk_ids: list[str] = Field(default_factory=list)
    acceptable_source_files: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    is_answerable: bool = True
    conflicts: list[str] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    sample_id: str
    question: str
    retrieved_ids: list[str] = Field(default_factory=list)
    retrieved_sources: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    latency_ms: float = 0.0


class MetricSummary(BaseModel):
    num_cases: int = 0
    top_k: list[int] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
