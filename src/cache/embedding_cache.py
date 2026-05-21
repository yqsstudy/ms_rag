"""L3 Embedding cache"""

import hashlib
import logging
import re
import time
import unicodedata
from typing import Dict, List, Optional

logger = logging.getLogger("ms_rag")


class EmbeddingCacheEntry:
    """Embedding cache entry"""

    __slots__ = ("key", "embedding", "created_at", "ttl")

    def __init__(self, key: str, embedding: List[float], created_at: float, ttl: int):
        self.key = key
        self.embedding = embedding
        self.created_at = created_at
        self.ttl = ttl

    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl


class EmbeddingCache:
    """Cache for query embeddings"""

    def __init__(self, max_size: int = 2000, ttl_seconds: int = 7200):
        self.cache: Dict[str, EmbeddingCacheEntry] = {}
        self.max_size = max_size
        self.ttl = ttl_seconds

    def get(self, query: str) -> Optional[List[float]]:
        key = self._make_key(query)
        entry = self.cache.get(key)
        if entry and not entry.is_expired():
            return entry.embedding
        if entry:
            del self.cache[key]
        return None

    def put(self, query: str, embedding: List[float]):
        key = self._make_key(query)
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = EmbeddingCacheEntry(
            key=key,
            embedding=embedding,
            created_at=time.time(),
            ttl=self.ttl,
        )

    def clear(self):
        count = len(self.cache)
        self.cache.clear()
        logger.info(f"[L3 Cache] Cleared {count} entries")

    @property
    def size(self) -> int:
        return len(self.cache)

    def _make_key(self, query: str) -> str:
        normalized = query.strip().lower()
        normalized = unicodedata.normalize("NFKC", normalized)
        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = re.sub(r"\s+", " ", normalized)
        return hashlib.md5(normalized.encode()).hexdigest()

    def _evict_oldest(self):
        if not self.cache:
            return
        oldest_key = min(self.cache, key=lambda k: self.cache[k].created_at)
        del self.cache[oldest_key]
