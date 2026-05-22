"""Chunk loading helpers for evaluation dataset generation."""

from __future__ import annotations

from pathlib import Path

from src.core.config import get_settings
from src.storage.keyword_index import BM25Index

from .config import RagEvalConfig
from .schemas import ChunkRecord


class ChunkSource:
    def __init__(self, config: RagEvalConfig):
        self.config = config
        self.settings = get_settings(config.paths.system_config)
        self.keyword_index = BM25Index(
            k1=self.settings.keyword_index.k1,
            b=self.settings.keyword_index.b,
        )
        if not self.keyword_index.load():
            raise FileNotFoundError("BM25 index not found. Run scripts/build_index.py first.")
        self._chunks = self._load_chunks()
        self._by_id = {chunk.chunk_id: chunk for chunk in self._chunks}
        self._by_doc: dict[str, list[ChunkRecord]] = {}
        for chunk in self._chunks:
            self._by_doc.setdefault(chunk.doc_id, []).append(chunk)

    def _load_chunks(self) -> list[ChunkRecord]:
        records = []
        raw_chunks = getattr(self.keyword_index, "_chunks", [])
        for index, chunk in enumerate(raw_chunks):
            prev_id = raw_chunks[index - 1].chunk_id if index > 0 else None
            next_id = raw_chunks[index + 1].chunk_id if index + 1 < len(raw_chunks) else None
            source_file = chunk.source_url or chunk.doc_id
            section_path = " > ".join(part for part in [chunk.doc_title, chunk.section_title] if part)
            records.append(
                ChunkRecord(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    source_file=source_file,
                    doc_title=chunk.doc_title,
                    section_title=chunk.section_title,
                    section_path=section_path,
                    content=chunk.content,
                    parent_id=getattr(chunk, "parent_id", "") or "",
                    prev_chunk_id=prev_id,
                    next_chunk_id=next_id,
                )
            )
        return records

    def chunks(self, limit: int | None = None, offset: int = 0) -> list[ChunkRecord]:
        chunks = self._chunks[offset:]
        return chunks[:limit] if limit else chunks

    def get(self, chunk_id: str) -> ChunkRecord | None:
        return self._by_id.get(chunk_id)

    def neighbors(self, chunk_id: str, window: int) -> list[ChunkRecord]:
        chunk = self.get(chunk_id)
        if not chunk:
            return []
        doc_chunks = self._by_doc.get(chunk.doc_id, [])
        ids = [item.chunk_id for item in doc_chunks]
        if chunk_id not in ids:
            return []
        index = ids.index(chunk_id)
        start = max(0, index - window)
        end = min(len(doc_chunks), index + window + 1)
        return [item for item in doc_chunks[start:end] if item.chunk_id != chunk_id]

    def same_section(self, chunk_id: str, limit: int) -> list[ChunkRecord]:
        chunk = self.get(chunk_id)
        if not chunk:
            return []
        matches = [
            item for item in self._by_doc.get(chunk.doc_id, [])
            if item.section_title == chunk.section_title and item.chunk_id != chunk_id
        ]
        return matches[:limit]

    def title_matches(self, keywords: list[str], limit: int) -> list[ChunkRecord]:
        lowered = [kw.lower() for kw in keywords if kw]
        matches = []
        for chunk in self._chunks:
            haystack = f"{chunk.doc_title} {chunk.section_title}".lower()
            if any(keyword.lower() in haystack for keyword in lowered):
                matches.append(chunk)
            if len(matches) >= limit:
                break
        return matches

    def require_index(self) -> None:
        if not Path(self.settings.vector_store.persist_directory).exists():
            raise FileNotFoundError("Vector store directory not found. Run scripts/build_index.py first.")
