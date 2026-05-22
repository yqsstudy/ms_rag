"""Build high-recall candidate evidence pools."""

from __future__ import annotations

from src.core.config import get_settings
from src.embeddings.embedding import EmbeddingService
from src.storage.keyword_index import BM25Index
from src.storage.vector_store import VectorStore

from .chunk_source import ChunkSource
from .config import RagEvalConfig
from .io import append_jsonl, read_jsonl, write_failed_record
from .schemas import CandidateChunk, CandidatePool, GeneratedQuestion


class EvidencePoolBuilder:
    def __init__(self, config: RagEvalConfig):
        self.config = config
        self.settings = get_settings(config.paths.system_config)
        self.chunk_source = ChunkSource(config)
        self.keyword_index = BM25Index(k1=self.settings.keyword_index.k1, b=self.settings.keyword_index.b)
        if not self.keyword_index.load():
            raise FileNotFoundError("BM25 index not found. Run scripts/build_index.py first.")
        self.vector_store = VectorStore(
            persist_directory=self.settings.vector_store.persist_directory,
            collection_name=self.settings.vector_store.collection_name,
        )
        self.embedding_service = EmbeddingService(
            model_name=self.settings.embedding.model,
            device=self.settings.embedding.device,
            normalize=self.settings.embedding.normalize,
        )

    def build(self, limit: int | None = None, offset: int = 0) -> int:
        input_path = self.config.output_dir / "questions.jsonl"
        output_path = self.config.output_dir / "candidate_pools.jsonl"
        questions = read_jsonl(input_path, GeneratedQuestion)[offset:]
        if limit:
            questions = questions[:limit]
        written = 0
        for question in questions:
            try:
                pool = self._build_one(question)
                append_jsonl(output_path, [pool])
                written += 1
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, "build_evidence_pool", question.model_dump(), str(exc))
        return written

    def _build_one(self, question: GeneratedQuestion) -> CandidatePool:
        candidates: dict[str, CandidateChunk] = {}

        def add(chunk_id: str, origin: str, **kwargs) -> None:
            chunk = self.chunk_source.get(chunk_id)
            if not chunk:
                return
            item = candidates.get(chunk_id)
            if not item:
                item = CandidateChunk(chunk_id=chunk_id, source_file=chunk.source_file)
                candidates[chunk_id] = item
            if origin not in item.origin:
                item.origin.append(origin)
            for key, value in kwargs.items():
                setattr(item, key, value)

        add(question.seed_chunk_id, "seed")
        for chunk_id in question.seed_chunk_ids:
            if chunk_id != question.seed_chunk_id:
                add(chunk_id, "scope_seed", same_doc=True)
        for chunk in self.chunk_source.neighbors(
            question.seed_chunk_id,
            self.config.candidate_pool.neighbor_window,
        ):
            add(chunk.chunk_id, "neighbor", seed_neighbor=True)
        for chunk in self.chunk_source.same_section(
            question.seed_chunk_id,
            self.config.candidate_pool.same_section_limit,
        ):
            add(chunk.chunk_id, "same_section", same_doc=True)
        for chunk in self.chunk_source.title_matches(
            question.keywords,
            self.config.candidate_pool.title_match_top_k,
        ):
            add(chunk.chunk_id, "title_match", title_match=True)

        bm25_results = self.keyword_index.search(question.question, k=self.config.candidate_pool.bm25_top_k)
        for rank, result in enumerate(bm25_results, start=1):
            add(
                result["chunk_id"],
                "bm25",
                bm25_score=float(result.get("score", 0.0)),
                bm25_rank=rank,
            )

        query_embedding = self.embedding_service.embed_query(question.question)
        vector_results = self.vector_store.search(
            query_embedding,
            k=self.config.candidate_pool.vector_top_k,
        )
        for rank, result in enumerate(vector_results, start=1):
            add(
                result.chunk_id,
                "vector",
                vector_score=float(result.score),
                vector_rank=rank,
            )

        return CandidatePool(
            question_id=question.id,
            question=question.question,
            seed_chunk_id=question.seed_chunk_id,
            candidate_chunks=list(candidates.values()),
        )
