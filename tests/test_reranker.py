"""Test reranker implementations."""

import sys
import types

from src.core.config import RetrievalConfig
from src.retrieval.hybrid_retriever import HybridResult
from src.retrieval.reranker import CrossEncoderReranker, Reranker, create_reranker


def make_result(chunk_id: str, content: str, vector_score: float = 0.0, keyword_score: float = 0.0) -> HybridResult:
    return HybridResult(
        chunk_id=chunk_id,
        doc_id=chunk_id,
        doc_title="工具使用",
        section_title="章节",
        content=content,
        source_url="",
        vector_score=vector_score,
        keyword_score=keyword_score,
    )


def test_heuristic_reranker_keeps_legacy_signature():
    results = [
        make_result("low", "短", vector_score=0.1, keyword_score=0.0),
        make_result("high", "这是一段更相关的内容" * 20, vector_score=0.9, keyword_score=8.0),
    ]

    reranked = Reranker().rerank(results)

    assert reranked[0].chunk_id == "high"


def test_heuristic_reranker_accepts_query():
    results = [
        make_result("low", "短", vector_score=0.1, keyword_score=0.0),
        make_result("high", "这是一段更相关的内容" * 20, vector_score=0.9, keyword_score=8.0),
    ]

    reranked = Reranker().rerank(results, "如何使用工具？")

    assert reranked[0].chunk_id == "high"


def test_create_reranker_defaults_to_heuristic():
    reranker = create_reranker(RetrievalConfig())

    assert isinstance(reranker, Reranker)


def test_cross_encoder_reranker_uses_query_passage_scores(monkeypatch):
    class FakeCrossEncoder:
        def __init__(self, model_name):
            self.model_name = model_name

        def predict(self, pairs):
            return [0.1 if "不相关" in passage else 0.9 for _, passage in pairs]

    fake_module = types.ModuleType("sentence_transformers")
    fake_module.CrossEncoder = FakeCrossEncoder
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)

    results = [
        make_result("bad", "不相关内容"),
        make_result("good", "通信耗时定位方法"),
    ]

    reranked = CrossEncoderReranker("fake-model").rerank(results, "如何定位通信耗时？")

    assert reranked[0].chunk_id == "good"
    assert reranked[0].final_score == 0.9


def test_cross_encoder_reranker_falls_back_without_query(monkeypatch):
    class FakeCrossEncoder:
        def __init__(self, model_name):
            self.model_name = model_name

    fake_module = types.ModuleType("sentence_transformers")
    fake_module.CrossEncoder = FakeCrossEncoder
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)

    results = [
        make_result("low", "短", vector_score=0.1, keyword_score=0.0),
        make_result("high", "这是一段更相关的内容" * 20, vector_score=0.9, keyword_score=8.0),
    ]

    reranked = CrossEncoderReranker("fake-model").rerank(results)

    assert reranked[0].chunk_id == "high"
