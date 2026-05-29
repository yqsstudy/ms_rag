"""Reranker for search results"""

import logging
from typing import Any, List, Literal

from .hybrid_retriever import HybridResult

logger = logging.getLogger("ms_rag")


class Reranker:
    """Reranker for search results"""

    def __init__(
        self,
        semantic_weight: float = 0.4,
        keyword_weight: float = 0.3,
        authority_weight: float = 0.2,
        completeness_weight: float = 0.1,
    ):
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        self.authority_weight = authority_weight
        self.completeness_weight = completeness_weight

        self.authority_scores = {
            "简介": 1.0,
            "概述": 1.0,
            "定位流程": 0.9,
            "工具使用": 0.9,
            "性能分析": 0.9,
            "问题解决方案": 0.8,
            "优化方案": 0.8,
            "案例分析": 0.7,
            "案例": 0.7,
        }

    def rerank(self, results: List[HybridResult], query: str | None = None) -> List[HybridResult]:
        """Rerank search results"""
        for result in results:
            score = 0.0
            score += self._semantic_score(result) * self.semantic_weight
            score += self._keyword_score(result) * self.keyword_weight
            score += self._authority_score(result) * self.authority_weight
            score += self._completeness_score(result) * self.completeness_weight
            result.final_score = score

        return sorted(results, key=lambda x: x.final_score, reverse=True)

    def _semantic_score(self, result: HybridResult) -> float:
        """Get semantic similarity score"""
        return result.vector_score

    def _keyword_score(self, result: HybridResult) -> float:
        """Get keyword match score"""
        return min(result.keyword_score / 10.0, 1.0)

    def _authority_score(self, result: HybridResult) -> float:
        """Get document authority score"""
        doc_title = result.doc_title
        section_title = result.section_title

        for key, score in self.authority_scores.items():
            if key in doc_title or key in section_title:
                return score

        return 0.6

    def _completeness_score(self, result: HybridResult) -> float:
        """Get content completeness score"""
        content_length = len(result.content)

        if content_length < 200:
            return 0.3
        if content_length < 500:
            return 0.5
        if content_length < 1000:
            return 0.7
        if content_length < 2000:
            return 0.9
        return 1.0


class CrossEncoderReranker:
    """Query-passage reranker backed by sentence-transformers CrossEncoder."""

    def __init__(
        self,
        model_name: str,
        fallback_reranker: Reranker | None = None,
        fallback_mode: Literal["heuristic", "none"] = "heuristic",
    ):
        self.model_name = model_name
        self.fallback_reranker = fallback_reranker or Reranker()
        self.fallback_mode = fallback_mode
        self.model = self._load_model(model_name)

    def rerank(self, results: List[HybridResult], query: str | None = None) -> List[HybridResult]:
        """Rerank search results by query-passage relevance."""
        if not results:
            return results
        if not query or not query.strip():
            return self._fallback(results, "missing query")
        if self.model is None:
            return self._fallback(results, "cross-encoder model unavailable")

        try:
            pairs = [(query, self._passage(result)) for result in results]
            scores = self.model.predict(pairs)
            for result, score in zip(results, scores):
                result.final_score = float(score)
            return sorted(results, key=lambda item: item.final_score, reverse=True)
        except Exception as exc:  # noqa: BLE001
            logger.warning("[Reranker] Cross-encoder rerank failed: %s", exc)
            return self._fallback(results, "cross-encoder inference failed")

    def _load_model(self, model_name: str) -> Any | None:
        try:
            from sentence_transformers import CrossEncoder

            logger.info("[Reranker] Loading cross-encoder reranker: %s", model_name)
            return CrossEncoder(model_name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("[Reranker] Cross-encoder unavailable: %s", exc)
            return None

    def _fallback(self, results: List[HybridResult], reason: str) -> List[HybridResult]:
        if self.fallback_mode == "heuristic":
            logger.info("[Reranker] Falling back to heuristic reranker: %s", reason)
            return self.fallback_reranker.rerank(results)
        logger.info("[Reranker] Keeping original order: %s", reason)
        return results

    def _passage(self, result: HybridResult) -> str:
        return "\n".join(
            part for part in (result.doc_title, result.section_title, result.content) if part
        )


def create_reranker(config: Any) -> Reranker | CrossEncoderReranker:
    """Create a reranker from retrieval config."""
    mode = getattr(config, "reranker_mode", "heuristic")
    if mode == "cross_encoder":
        return CrossEncoderReranker(
            model_name=getattr(config, "reranker_model", "BAAI/bge-reranker-base"),
            fallback_mode=getattr(config, "reranker_fallback", "heuristic"),
        )
    return Reranker()
