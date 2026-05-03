"""Reranker for search results"""

from typing import List

from .hybrid_retriever import HybridResult


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

        # Document authority scores by type
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

    def rerank(self, results: List[HybridResult]) -> List[HybridResult]:
        """Rerank search results"""
        for result in results:
            score = 0.0

            # Semantic score (from vector search)
            score += self._semantic_score(result) * self.semantic_weight

            # Keyword match score
            score += self._keyword_score(result) * self.keyword_weight

            # Authority score
            score += self._authority_score(result) * self.authority_weight

            # Completeness score
            score += self._completeness_score(result) * self.completeness_weight

            result.final_score = score

        # Sort by final score
        return sorted(results, key=lambda x: x.final_score, reverse=True)

    def _semantic_score(self, result: HybridResult) -> float:
        """Get semantic similarity score"""
        return result.vector_score

    def _keyword_score(self, result: HybridResult) -> float:
        """Get keyword match score"""
        # Normalize keyword score (BM25 scores can be large)
        return min(result.keyword_score / 10.0, 1.0)

    def _authority_score(self, result: HybridResult) -> float:
        """Get document authority score"""
        doc_title = result.doc_title
        section_title = result.section_title

        # Check both doc title and section title
        for key, score in self.authority_scores.items():
            if key in doc_title or key in section_title:
                return score

        return 0.6  # Default score

    def _completeness_score(self, result: HybridResult) -> float:
        """Get content completeness score"""
        content_length = len(result.content)

        # Score based on content length
        if content_length < 200:
            return 0.3
        elif content_length < 500:
            return 0.5
        elif content_length < 1000:
            return 0.7
        elif content_length < 2000:
            return 0.9
        else:
            return 1.0