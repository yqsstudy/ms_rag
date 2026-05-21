"""L1 Exact match cache"""

import hashlib
import logging
import re
import time
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger("ms_rag")


@dataclass
class CacheEntry:
    """Cache entry"""

    key: str
    response: dict
    metadata: dict
    created_at: float
    ttl: int
    hit_count: int = 0

    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl


class ExactCache:
    """Exact match cache based on normalized query hash"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl = ttl_seconds

    def get(self, query: str) -> Optional[CacheEntry]:
        key = self._make_key(query)
        entry = self.cache.get(key)
        if entry and not entry.is_expired():
            entry.hit_count += 1
            return entry
        if entry:
            del self.cache[key]
        return None

    def put(self, query: str, response: dict, metadata: dict = None):
        key = self._make_key(query)
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = CacheEntry(
            key=key,
            response=response,
            metadata=metadata or {},
            created_at=time.time(),
            ttl=self.ttl,
        )

    def invalidate_by_doc(self, doc_ids: List[str]):
        keys_to_remove = []
        for key, entry in self.cache.items():
            source_doc_ids = [s.get("doc_id") for s in entry.response.get("sources", [])]
            if any(did in source_doc_ids for did in doc_ids):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.cache[key]
        if keys_to_remove:
            logger.info(f"[L1 Cache] Invalidated {len(keys_to_remove)} entries for docs: {doc_ids}")

    def clear(self):
        count = len(self.cache)
        self.cache.clear()
        logger.info(f"[L1 Cache] Cleared {count} entries")

    @property
    def size(self) -> int:
        return len(self.cache)

    def _make_key(self, query: str) -> str:
        normalized = self._normalize(query)
        return hashlib.md5(normalized.encode()).hexdigest()

    @staticmethod
    def _normalize(query: str) -> str:
        text = query.strip().lower()
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def _evict_oldest(self):
        if not self.cache:
            return
        oldest_key = min(self.cache, key=lambda k: self.cache[k].created_at)
        del self.cache[oldest_key]
