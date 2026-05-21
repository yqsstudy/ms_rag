"""L2 Semantic similarity cache"""

import hashlib
import logging
import re
import time
import unicodedata
from typing import Dict, List, Optional

import numpy as np

from .exact_cache import CacheEntry

logger = logging.getLogger("ms_rag")


class SemanticCache:
    """Semantic similarity cache using vector cosine similarity"""

    def __init__(
        self,
        max_size: int = 500,
        ttl_seconds: int = 1800,
        similarity_threshold: float = 0.92,
    ):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.threshold = similarity_threshold

        self.vectors: Dict[str, np.ndarray] = {}
        self.entries: Dict[str, CacheEntry] = {}

    def get(self, query: str, query_embedding: List[float]) -> Optional[CacheEntry]:
        if not self.vectors:
            return None

        self._clean_expired()

        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm < 1e-8:
            return None
        query_vec = query_vec / query_norm

        best_score = 0.0
        best_key = None

        for key, vec in self.vectors.items():
            vec_norm = np.linalg.norm(vec)
            if vec_norm < 1e-8:
                continue
            score = float(np.dot(query_vec, vec / vec_norm))
            if score > best_score:
                best_score = score
                best_key = key

        if best_score >= self.threshold and best_key in self.entries:
            entry = self.entries[best_key]
            if not entry.is_expired():
                entry.hit_count += 1
                return entry
            else:
                self._remove(best_key)

        return None

    def put(self, query: str, query_embedding: List[float], response: dict):
        key = self._make_key(query)
        if len(self.entries) >= self.max_size:
            self._evict_oldest()
        self.vectors[key] = np.array(query_embedding, dtype=np.float32)
        self.entries[key] = CacheEntry(
            key=key,
            response=response,
            metadata={"original_query": query},
            created_at=time.time(),
            ttl=self.ttl,
        )

    def invalidate_by_doc(self, doc_ids: List[str]):
        keys_to_remove = []
        for key, entry in self.entries.items():
            source_doc_ids = [s.get("doc_id") for s in entry.response.get("sources", [])]
            if any(did in source_doc_ids for did in doc_ids):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self._remove(key)
        if keys_to_remove:
            logger.info(f"[L2 Cache] Invalidated {len(keys_to_remove)} entries for docs: {doc_ids}")

    def clear(self):
        count = len(self.entries)
        self.vectors.clear()
        self.entries.clear()
        logger.info(f"[L2 Cache] Cleared {count} entries")

    @property
    def size(self) -> int:
        return len(self.entries)

    def _remove(self, key: str):
        self.vectors.pop(key, None)
        self.entries.pop(key, None)

    def _clean_expired(self):
        expired_keys = [k for k, e in self.entries.items() if e.is_expired()]
        for key in expired_keys:
            self._remove(key)

    def _make_key(self, query: str) -> str:
        normalized = query.strip().lower()
        normalized = unicodedata.normalize("NFKC", normalized)
        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = re.sub(r"\s+", " ", normalized)
        return hashlib.md5(normalized.encode()).hexdigest()

    def _evict_oldest(self):
        if not self.entries:
            return
        oldest_key = min(self.entries, key=lambda k: self.entries[k].created_at)
        self._remove(oldest_key)
