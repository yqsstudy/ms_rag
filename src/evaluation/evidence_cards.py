"""Build compact evidence cards from candidate pools."""

from __future__ import annotations

import jieba

from .chunk_source import ChunkSource
from .config import RagEvalConfig
from .io import append_jsonl, read_jsonl, write_failed_record
from .schemas import CandidateChunk, CandidatePool, EvidenceCard, EvidenceCardSet


class EvidenceCardBuilder:
    def __init__(self, config: RagEvalConfig):
        self.config = config
        self.chunk_source = ChunkSource(config)

    def build(self, limit: int | None = None, offset: int = 0) -> int:
        input_path = self.config.output_dir / "candidate_pools.jsonl"
        output_path = self.config.output_dir / "evidence_cards.jsonl"
        pools = read_jsonl(input_path, CandidatePool)[offset:]
        if limit:
            pools = pools[:limit]
        written = 0
        for pool in pools:
            try:
                cards = self._build_one(pool)
                append_jsonl(output_path, [cards])
                written += 1
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, "build_evidence_cards", pool.model_dump(), str(exc))
        return written

    def _build_one(self, pool: CandidatePool) -> EvidenceCardSet:
        ranked = self._rank(pool.candidate_chunks)
        cards = []
        per_source: dict[str, int] = {}
        keywords = self._keywords(pool.question)
        for candidate, score in ranked:
            chunk = self.chunk_source.get(candidate.chunk_id)
            if not chunk:
                continue
            source_count = per_source.get(chunk.source_file, 0)
            if source_count >= self.config.card_filter.max_chunks_per_source:
                continue
            per_source[chunk.source_file] = source_count + 1
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
            if len(cards) >= self.config.card_filter.max_cards_per_question:
                break
        return EvidenceCardSet(
            question_id=pool.question_id,
            question=pool.question,
            seed_chunk_id=pool.seed_chunk_id,
            cards=cards,
        )

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
