"""Build compact evidence cards from candidate pools."""

from __future__ import annotations

from collections import defaultdict

import jieba

from .chunk_source import ChunkSource
from .config import RagEvalConfig
from .io import append_jsonl, load_existing_ids, read_jsonl, write_failed_record, write_jsonl
from .schemas import CandidateChunk, CandidatePool, ChunkRecord, EvidenceCard, EvidenceCardSet


class EvidenceCardBuilder:
    def __init__(self, config: RagEvalConfig):
        self.config = config
        self.chunk_source = ChunkSource(config)

    def build(self, limit: int | None = None, offset: int = 0, force: bool = False) -> int:
        input_path = self.config.output_dir / "candidate_pools.jsonl"
        output_path = self.config.output_dir / "evidence_cards.jsonl"
        if force:
            write_jsonl(output_path, [])
        existing = set() if force else load_existing_ids(output_path, "question_id")
        pools = read_jsonl(input_path, CandidatePool)[offset:]
        if limit:
            pools = pools[:limit]
        written = 0
        for pool in pools:
            if pool.question_id in existing:
                continue
            try:
                cards = self._build_one(pool)
                append_jsonl(output_path, [cards])
                existing.add(pool.question_id)
                written += 1
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, "build_evidence_cards", pool.model_dump(), str(exc))
        return written

    def _build_one(self, pool: CandidatePool) -> EvidenceCardSet:
        ranked = self._rank(pool.candidate_chunks)
        selected = self._select_candidates(pool, ranked)
        keywords = self._keywords(pool.question)
        cards = []
        for candidate, score, chunk in selected:
            cards.append(
                EvidenceCard(
                    chunk_id=chunk.chunk_id,
                    source_file=chunk.source_file,
                    doc_title=chunk.doc_title,
                    section_path=chunk.section_path,
                    matched_keywords=[kw for kw in keywords if kw.lower() in chunk.content.lower()],
                    snippet=self._snippet(chunk.content),
                    bm25_rank=candidate.bm25_rank,
                    vector_rank=candidate.vector_rank,
                    score=score,
                )
            )
        return EvidenceCardSet(
            question_id=pool.question_id,
            question=pool.question,
            seed_chunk_id=pool.seed_chunk_id,
            question_scope=pool.question_scope,
            cards=cards,
        )

    def _select_candidates(
        self,
        pool: CandidatePool,
        ranked: list[tuple[CandidateChunk, float]],
    ) -> list[tuple[CandidateChunk, float, ChunkRecord]]:
        resolved = self._resolve_ranked(ranked)
        if pool.question_scope == "document":
            return self._coverage_select(resolved, self._document_bucket_key, per_bucket_limit=3)
        if pool.question_scope == "section":
            return self._coverage_select(resolved, self._section_bucket_key, per_bucket_limit=2)
        return self._top_select(resolved)

    def _resolve_ranked(
        self,
        ranked: list[tuple[CandidateChunk, float]],
    ) -> list[tuple[CandidateChunk, float, ChunkRecord]]:
        resolved = []
        for candidate, score in ranked:
            chunk = self.chunk_source.get(candidate.chunk_id)
            if chunk:
                resolved.append((candidate, score, chunk))
        return resolved

    def _top_select(
        self,
        resolved: list[tuple[CandidateChunk, float, ChunkRecord]],
    ) -> list[tuple[CandidateChunk, float, ChunkRecord]]:
        selected = []
        per_source: dict[str, int] = {}
        for item in resolved:
            if self._append_selected(selected, per_source, item):
                if len(selected) >= self.config.card_filter.max_cards_per_question:
                    break
        return selected

    def _coverage_select(
        self,
        resolved: list[tuple[CandidateChunk, float, ChunkRecord]],
        bucket_key,
        per_bucket_limit: int,
    ) -> list[tuple[CandidateChunk, float, ChunkRecord]]:
        selected = []
        selected_ids = set()
        per_source: dict[str, int] = {}
        buckets = defaultdict(list)
        for item in resolved:
            buckets[bucket_key(item[2])].append(item)

        for bucket_items in sorted(buckets.values(), key=lambda items: items[0][1], reverse=True):
            added = 0
            for item in bucket_items:
                if item[0].chunk_id in selected_ids:
                    continue
                if self._append_selected(selected, per_source, item):
                    selected_ids.add(item[0].chunk_id)
                    added += 1
                if added >= per_bucket_limit or len(selected) >= self.config.card_filter.max_cards_per_question:
                    break
            if len(selected) >= self.config.card_filter.max_cards_per_question:
                return selected

        for item in resolved:
            if item[0].chunk_id in selected_ids:
                continue
            if self._append_selected(selected, per_source, item):
                selected_ids.add(item[0].chunk_id)
            if len(selected) >= self.config.card_filter.max_cards_per_question:
                break
        return selected

    def _append_selected(
        self,
        selected: list[tuple[CandidateChunk, float, ChunkRecord]],
        per_source: dict[str, int],
        item: tuple[CandidateChunk, float, ChunkRecord],
    ) -> bool:
        chunk = item[2]
        source_count = per_source.get(chunk.source_file, 0)
        if source_count >= self.config.card_filter.max_chunks_per_source:
            return False
        per_source[chunk.source_file] = source_count + 1
        selected.append(item)
        return True

    def _document_bucket_key(self, chunk: ChunkRecord) -> str:
        return chunk.section_path or chunk.section_title or chunk.parent_id or chunk.chunk_id

    def _section_bucket_key(self, chunk: ChunkRecord) -> str:
        return chunk.parent_id or chunk.chunk_id

    def _rank(self, candidates: list[CandidateChunk]) -> list[tuple[CandidateChunk, float]]:
        max_bm25 = max((item.bm25_score for item in candidates), default=0.0) or 1.0
        max_vector = max((item.vector_score for item in candidates), default=0.0) or 1.0
        scored = []
        for item in candidates:
            score = (
                self.config.card_filter.bm25_weight * (item.bm25_score / max_bm25)
                + self.config.card_filter.vector_weight * (item.vector_score / max_vector)
            )
            if item.title_match:
                score += self.config.card_filter.title_match_bonus
            if item.same_doc:
                score += self.config.card_filter.same_doc_bonus
            if item.seed_neighbor or "seed" in item.origin:
                score += self.config.card_filter.seed_neighbor_bonus
            scored.append((item, score))
        return sorted(scored, key=lambda pair: pair[1], reverse=True)

    def _snippet(self, content: str) -> str:
        text = " ".join(content.split())
        limit = self.config.card_filter.snippet_chars
        return text[:limit] + ("..." if len(text) > limit else "")

    def _keywords(self, question: str) -> list[str]:
        return [word for word in jieba.lcut(question) if len(word.strip()) > 1]
