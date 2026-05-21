"""Multi-level cache manager"""

import logging
import time
from dataclasses import dataclass
from typing import List, Optional

from ..core.config import CacheConfig
from ..embeddings.embedding import EmbeddingService
from .embedding_cache import EmbeddingCache
from .exact_cache import ExactCache
from .semantic_cache import SemanticCache

logger = logging.getLogger("ms_rag")


@dataclass
class CacheStats:
    """Cache statistics"""

    l1_hits: int = 0
    l1_misses: int = 0
    l2_hits: int = 0
    l2_misses: int = 0
    l3_hits: int = 0
    l3_misses: int = 0

    @property
    def total_requests(self) -> int:
        return self.l1_hits + self.l1_misses

    @property
    def l1_hit_rate(self) -> float:
        total = self.l1_hits + self.l1_misses
        return self.l1_hits / total if total > 0 else 0.0

    @property
    def l2_hit_rate(self) -> float:
        total = self.l2_hits + self.l2_misses
        return self.l2_hits / total if total > 0 else 0.0

    @property
    def l3_hit_rate(self) -> float:
        total = self.l3_hits + self.l3_misses
        return self.l3_hits / total if total > 0 else 0.0


class CacheManager:
    """Multi-level cache manager: L1 exact -> L2 semantic -> L3 embedding"""

    def __init__(self, config: CacheConfig, embedding_service: EmbeddingService):
        self.enabled = config.enabled
        self.embedding_service = embedding_service

        self.l1 = ExactCache(
            max_size=config.l1_max_size,
            ttl_seconds=config.l1_ttl,
        )
        self.l2 = SemanticCache(
            max_size=config.l2_max_size,
            ttl_seconds=config.l2_ttl,
            similarity_threshold=config.l2_threshold,
        )
        self.l3 = EmbeddingCache(
            max_size=config.l3_max_size,
            ttl_seconds=config.l3_ttl,
        )

        self.stats = CacheStats()
        self._request_count = 0

    def get(self, query: str, query_embedding: Optional[List[float]] = None) -> Optional[dict]:
        """Try to get cached response. Pass query_embedding to enable L2."""
        if not self.enabled:
            return None

        # L1: exact match
        entry = self.l1.get(query)
        if entry:
            self.stats.l1_hits += 1
            self._log_stats()
            response = entry.response.copy()
            response.setdefault("metadata", {})
            response["metadata"]["cache_level"] = "L1"
            response["metadata"]["cached"] = True
            return response
        self.stats.l1_misses += 1

        # L2: semantic similarity (needs embedding)
        if query_embedding is not None:
            entry = self.l2.get(query, query_embedding)
            if entry:
                self.stats.l2_hits += 1
                self._log_stats()
                response = entry.response.copy()
                response.setdefault("metadata", {})
                response["metadata"]["cache_level"] = "L2"
                response["metadata"]["cached"] = True
                return response
            self.stats.l2_misses += 1

        return None

    def get_embedding(self, query: str) -> Optional[List[float]]:
        """Get cached embedding from L3"""
        if not self.enabled:
            return None
        embedding = self.l3.get(query)
        if embedding:
            self.stats.l3_hits += 1
        else:
            self.stats.l3_misses += 1
        return embedding

    def put(self, query: str, query_embedding: List[float], response: dict):
        """Write response to L1 + L2, and embedding to L3"""
        if not self.enabled:
            return
        self.l1.put(query, response)
        self.l2.put(query, query_embedding, response)
        self.l3.put(query, query_embedding)

    def put_embedding(self, query: str, embedding: List[float]):
        """Write embedding to L3 only"""
        if not self.enabled:
            return
        self.l3.put(query, embedding)

    def invalidate_by_doc(self, doc_ids: List[str]):
        """Invalidate cache entries that reference given doc_ids"""
        self.l1.invalidate_by_doc(doc_ids)
        self.l2.invalidate_by_doc(doc_ids)
        logger.info(f"[Cache] Invalidated entries for docs: {doc_ids}")

    def clear(self, level: str = "all"):
        """Clear cache. level: 'all', 'l1', 'l2', 'l3'"""
        if level in ("all", "l1"):
            self.l1.clear()
        if level in ("all", "l2"):
            self.l2.clear()
        if level in ("all", "l3"):
            self.l3.clear()
        logger.info(f"[Cache] Cleared cache level={level}")

    def get_stats(self) -> dict:
        return {
            "l1_hit_rate": f"{self.stats.l1_hit_rate:.1%}",
            "l2_hit_rate": f"{self.stats.l2_hit_rate:.1%}",
            "l3_hit_rate": f"{self.stats.l3_hit_rate:.1%}",
            "l1_size": self.l1.size,
            "l2_size": self.l2.size,
            "l3_size": self.l3.size,
            "total_requests": self.stats.total_requests,
        }

    def _log_stats(self):
        self._request_count += 1
        if self._request_count % 100 == 0:
            stats = self.get_stats()
            logger.info(
                f"[Cache Stats] L1={stats['l1_hit_rate']} L2={stats['l2_hit_rate']} "
                f"L3={stats['l3_hit_rate']} total={stats['total_requests']}"
            )
