"""Hybrid retriever combining vector and keyword search"""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Optional

from ..storage.keyword_index import BM25Index
from ..storage.vector_store import SearchResult, VectorStore

from ..storage.document_store import DocumentStore

logger = logging.getLogger("ms_rag")


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
    parent_id: Optional[str] = None

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
        document_store: Optional[DocumentStore] = None,
        vector_weight: float = 0.6,
        keyword_weight: float = 0.4,
    ):
        self.vector_store = vector_store
        self.keyword_index = keyword_index
        self.document_store = document_store
        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight

    async def aretrieve(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 10,
    ) -> List[HybridResult]:
        """Retrieve documents using hybrid search concurrently"""
        import asyncio
        t0 = time.time()

        # Concurrent vector and keyword search
        vector_task = self.vector_store.asearch(query_embedding, k=k * 2)
        keyword_task = self.keyword_index.asearch(query, k=k * 2)
        
        vector_results, keyword_results = await asyncio.gather(vector_task, keyword_task)
        
        logger.debug(f"[Retriever] Vector search returned {len(vector_results)} results")
        logger.debug(f"[Retriever] Keyword search returned {len(keyword_results)} results")

        # Merge and rank using RRF (Reciprocal Rank Fusion)
        merged = self._merge_results(vector_results, keyword_results)

        logger.debug(f"[Retriever] Merged {len(merged)} results in {time.time()-t0:.3f}s")
        return merged[:k]

    def retrieve(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 10,
    ) -> List[HybridResult]:
        """Retrieve documents using hybrid search"""
        t0 = time.time()

        # Vector search
        vector_results = self.vector_store.search(query_embedding, k=k * 2)
        logger.debug(f"[Retriever] Vector search returned {len(vector_results)} results")

        # Keyword search
        keyword_results = self.keyword_index.search(query, k=k * 2)
        logger.debug(f"[Retriever] Keyword search returned {len(keyword_results)} results")

        # Merge and rank using RRF (Reciprocal Rank Fusion)
        merged = self._merge_results(vector_results, keyword_results)

        logger.debug(f"[Retriever] Merged {len(merged)} results in {time.time()-t0:.3f}s")
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
                    images=result.metadata.get("images", []),
                    parent_id=result.metadata.get("parent_id", ""),
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
                    images=result.get("images", []),
                    parent_id=result.get("parent_id", ""),
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

        sorted_results = sorted(
            result_map.values(),
            key=lambda x: x.final_score,
            reverse=True,
        )

        if self.document_store:
            final_results = []
            seen_parents = set()
            
            for res in sorted_results:
                parent_id = res.parent_id
                if parent_id and parent_id not in seen_parents:
                    parent_doc = self.document_store.get_document(parent_id)
                    if parent_doc:
                        seen_parents.add(parent_id)
                        res.content = parent_doc.get("content", res.content)
                        res.images = parent_doc.get("images", res.images)
                        res.chunk_id = parent_id
                        final_results.append(res)
                elif not parent_id:
                    final_results.append(res)
            
            return final_results

        return sorted_results