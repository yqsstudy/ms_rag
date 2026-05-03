"""BM25 keyword index"""

import json
import pickle
from pathlib import Path
from typing import List, Optional

import jieba
from rank_bm25 import BM25Okapi

from ..data.splitter import Chunk


class BM25Index:
    """BM25 keyword index for text search"""

    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        index_path: str = "./data/indexes/bm25_index.pkl",
    ):
        self.k1 = k1
        self.b = b
        self.index_path = Path(index_path)
        self._bm25: Optional[BM25Okapi] = None
        self._chunks: List[Chunk] = []
        self._corpus: List[List[str]] = []

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text using jieba"""
        # Use jieba for Chinese text segmentation
        tokens = jieba.lcut(text)
        # Filter out single characters and punctuation
        return [t for t in tokens if len(t) > 1 and t.strip()]

    def build_index(self, chunks: List[Chunk]) -> None:
        """Build BM25 index from chunks"""
        self._chunks = chunks
        self._corpus = [self._tokenize(chunk.content) for chunk in chunks]
        self._bm25 = BM25Okapi(self._corpus, k1=self.k1, b=self.b)

    def search(self, query: str, k: int = 10) -> List[dict]:
        """Search for documents using BM25"""
        if self._bm25 is None:
            raise ValueError("Index not built. Call build_index() first.")

        query_tokens = self._tokenize(query)
        scores = self._bm25.get_scores(query_tokens)

        # Get top k results
        top_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:k]

        results = []
        for idx in top_indices:
            chunk = self._chunks[idx]
            results.append({
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "doc_title": chunk.doc_title,
                "section_title": chunk.section_title,
                "content": chunk.content,
                "source_url": chunk.source_url,
                "score": float(scores[idx]),
                "images": chunk.images,  # 包含图片信息
            })

        return results

    def save(self) -> None:
        """Save index to disk"""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump({
                "bm25": self._bm25,
                "chunks": [
                    (c.chunk_id, c.doc_id, c.doc_title, c.section_title,
                     c.content, c.source_url, c.parent_topic, c.images)
                    for c in self._chunks
                ],
                "corpus": self._corpus,
            }, f)

    def load(self) -> bool:
        """Load index from disk"""
        if not self.index_path.exists():
            return False

        with open(self.index_path, "rb") as f:
            data = pickle.load(f)
            self._bm25 = data["bm25"]
            self._chunks = [
                Chunk(
                    chunk_id=c[0],
                    doc_id=c[1],
                    doc_title=c[2],
                    section_title=c[3],
                    content=c[4],
                    source_url=c[5],
                    parent_topic=c[6],
                    images=c[7] if len(c) > 7 else [],  # 兼容旧版本
                )
                for c in data["chunks"]
            ]
            self._corpus = data["corpus"]

        return True

    def count(self) -> int:
        """Get number of documents in index"""
        return len(self._chunks) if self._chunks else 0

    def is_loaded(self) -> bool:
        """Check if index is loaded"""
        return self._bm25 is not None