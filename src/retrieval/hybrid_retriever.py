"""Hybrid retriever combining vector and keyword search"""

from dataclasses import dataclass, field
from typing import List, Optional

from ..storage.keyword_index import BM25Index
from ..storage.vector_store import SearchResult, VectorStore


@dataclass
class HybridResult:
    """Hybrid search result"""

    chunk_id: str
    doc_id: str
    doc_title: str
    section_title: str
    content: str
    source_url: str
    vector_score: float = 0.0
    keyword_score: float = 0.0
    final_score: float = 0.0
    parent_topic: Optional[str] = None
    images: list[dict] = field(default_factory=list)  # 新增图片字段

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "doc_title": self.doc_title,
            "section_title": self.section_title,
            "content": self.content,
            "source_url": self.source_url,
            "vector_score": self.vector_score,
            "keyword_score": self.keyword_score,
            "final_score": self.final_score,
            "parent_topic": self.parent_topic,
            "images": self.images,
        }


class HybridRetriever:
    """Hybrid retriever combining vector and keyword search"""

    def __init__(
        self,
        vector_store: VectorStore,
        keyword_index: BM25Index,
        vector_weight: float = 0.6,
        keyword_weight: float = 0.4,
    ):
        self.vector_store = vector_store
        self.keyword_index = keyword_index
        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight

    def retrieve(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 10,
    ) -> List[HybridResult]:
        """Retrieve documents using hybrid search"""
        # Vector search
        vector_results = self.vector_store.search(query_embedding, k=k * 2)

        # Keyword search
        keyword_results = self.keyword_index.search(query, k=k * 2)

        # Merge and rank using RRF (Reciprocal Rank Fusion)
        merged = self._merge_results(vector_results, keyword_results)

        return merged[:k]

    def _merge_results(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[dict],
    ) -> List[HybridResult]:
        """Merge results using Reciprocal Rank Fusion (RRF)"""
        # Create a map of chunk_id to result
        result_map: dict[str, HybridResult] = {}

        # Process vector results
        for rank, result in enumerate(vector_results):
            chunk_id = result.chunk_id
            if chunk_id not in result_map:
                result_map[chunk_id] = HybridResult(
                    chunk_id=chunk_id,
                    doc_id=result.metadata.get("doc_id", ""),
                    doc_title=result.metadata.get("doc_title", ""),
                    section_title=result.metadata.get("section_title", ""),
                    content=result.content,
                    source_url=result.metadata.get("source_url", ""),
                    parent_topic=result.metadata.get("parent_topic"),
                    images=result.metadata.get("images", []),  # 图片信息
                )
            result_map[chunk_id].vector_score = result.score

        # Process keyword results
        for rank, result in enumerate(keyword_results):
            chunk_id = result["chunk_id"]
            if chunk_id not in result_map:
                result_map[chunk_id] = HybridResult(
                    chunk_id=chunk_id,
                    doc_id=result.get("doc_id", ""),
                    doc_title=result.get("doc_title", ""),
                    section_title=result.get("section_title", ""),
                    content=result.get("content", ""),
                    source_url=result.get("source_url", ""),
                    images=result.get("images", []),  # 图片信息
                )
            result_map[chunk_id].keyword_score = result.get("score", 0.0)

        # Calculate final score using weighted combination
        for result in result_map.values():
            # Normalize scores
            vec_score = result.vector_score
            kw_score = result.keyword_score

            # Weighted combination
            result.final_score = (
                self.vector_weight * vec_score +
                self.keyword_weight * kw_score
            )

        # Sort by final score
        sorted_results = sorted(
            result_map.values(),
            key=lambda x: x.final_score,
            reverse=True,
        )

        return sorted_results