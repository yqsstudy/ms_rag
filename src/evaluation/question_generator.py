"""Generate candidate evaluation questions from chunks."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass

from .chunk_source import ChunkSource
from .config import RagEvalConfig
from .io import append_jsonl, load_existing_ids, save_raw_response, write_failed_record, write_jsonl
from .openai_client import OpenAICompatibleClient
from .prompt_templates import (
    GENERATE_DOCUMENT_QUESTIONS_SYSTEM,
    GENERATE_DOCUMENT_QUESTIONS_USER,
    GENERATE_QUESTIONS_SYSTEM,
    GENERATE_QUESTIONS_USER,
    GENERATE_SECTION_QUESTIONS_SYSTEM,
    GENERATE_SECTION_QUESTIONS_USER,
)
from .schemas import ChunkRecord, GeneratedQuestion


def stable_question_id(scope: str, seed_chunk_id: str, question: str) -> str:
    digest = hashlib.sha1(f"{scope}:{seed_chunk_id}:{question}".encode("utf-8")).hexdigest()[:12]
    return f"q_{digest}"


@dataclass
class QuestionSeed:
    scope: str
    seed_chunk_id: str
    seed_chunk_ids: list[str]
    source_file: str
    doc_id: str
    doc_title: str
    section_title: str
    section_path: str
    content: str
    raw_record: dict


class QuestionGenerator:
    def __init__(self, config: RagEvalConfig, client: OpenAICompatibleClient):
        self.config = config
        self.client = client
        self.chunk_source = ChunkSource(config)

    def generate(self, limit: int | None = None, offset: int = 0, force: bool = False) -> int:
        output_path = self.config.output_dir / "questions.jsonl"
        if force:
            write_jsonl(output_path, [])
        existing = set() if force else load_existing_ids(output_path)
        written = 0
        scopes = set(self.config.question_generation.enabled_scopes)
        chunks = self._load_chunks(limit=limit, offset=offset)

        if "chunk" in scopes:
            written += self._generate_for_seeds(output_path, existing, self._chunk_seeds(chunks))
        if "section" in scopes:
            written += self._generate_for_seeds(output_path, existing, self._section_seeds(chunks))
        if "document" in scopes:
            written += self._generate_for_seeds(output_path, existing, self._document_seeds(chunks))
        return written

    def _load_chunks(self, limit: int | None, offset: int) -> list[ChunkRecord]:
        chunks = self.chunk_source.chunks(limit=limit, offset=offset)
        if limit is None and self.config.question_generation.max_chunks:
            chunks = chunks[: self.config.question_generation.max_chunks]
        return chunks

    def _chunk_seeds(self, chunks: list[ChunkRecord]) -> list[QuestionSeed]:
        seeds = []
        for chunk in chunks:
            if len(chunk.content.strip()) < self.config.question_generation.min_chunk_chars:
                continue
            seeds.append(self._seed_from_chunks("chunk", [chunk], chunk.content[:3000], chunk.model_dump()))
        return seeds

    def _section_seeds(self, chunks: list[ChunkRecord]) -> list[QuestionSeed]:
        grouped: dict[tuple[str, str], list[ChunkRecord]] = defaultdict(list)
        for chunk in chunks:
            key = (chunk.doc_id, chunk.section_path or chunk.section_title or chunk.parent_id or chunk.chunk_id)
            grouped[key].append(chunk)

        seeds = []
        for group_chunks in grouped.values():
            content = self._representative_content(group_chunks)
            if len(content.strip()) < self.config.question_generation.min_section_chars:
                continue
            seeds.append(self._seed_from_chunks("section", group_chunks, content, self._group_record("section", group_chunks)))
            if len(seeds) >= self.config.question_generation.max_sections:
                break
        return seeds

    def _document_seeds(self, chunks: list[ChunkRecord]) -> list[QuestionSeed]:
        grouped: dict[str, list[ChunkRecord]] = defaultdict(list)
        for chunk in chunks:
            grouped[chunk.doc_id or chunk.source_file or chunk.chunk_id].append(chunk)

        seeds = []
        for group_chunks in grouped.values():
            content = self._representative_content(group_chunks)
            if len(content.strip()) < self.config.question_generation.min_document_chars:
                continue
            seeds.append(self._seed_from_chunks("document", group_chunks, content, self._group_record("document", group_chunks)))
            if len(seeds) >= self.config.question_generation.max_documents:
                break
        return seeds

    def _representative_content(self, chunks: list[ChunkRecord]) -> str:
        snippets = []
        for chunk in chunks[:8]:
            title = chunk.section_path or chunk.section_title
            prefix = f"[{title}]\n" if title else ""
            snippets.append(f"{prefix}{chunk.content[:700]}")
        return "\n\n---\n\n".join(snippets)[:5000]

    def _seed_from_chunks(self, scope: str, chunks: list[ChunkRecord], content: str, raw_record: dict) -> QuestionSeed:
        first = chunks[0]
        seed_ids = [chunk.chunk_id for chunk in chunks[:8]]
        section_titles = []
        for chunk in chunks:
            title = chunk.section_path or chunk.section_title
            if title and title not in section_titles:
                section_titles.append(title)
        return QuestionSeed(
            scope=scope,
            seed_chunk_id=first.chunk_id,
            seed_chunk_ids=seed_ids,
            source_file=first.source_file,
            doc_id=first.doc_id,
            doc_title=first.doc_title,
            section_title=first.section_title,
            section_path=" / ".join(section_titles[:8]) if scope == "document" else first.section_path,
            content=content,
            raw_record=raw_record,
        )

    def _group_record(self, scope: str, chunks: list[ChunkRecord]) -> dict:
        first = chunks[0]
        return {
            "scope": scope,
            "seed_chunk_id": first.chunk_id,
            "seed_chunk_ids": [chunk.chunk_id for chunk in chunks[:8]],
            "doc_id": first.doc_id,
            "doc_title": first.doc_title,
            "section_title": first.section_title,
            "section_path": first.section_path,
            "source_file": first.source_file,
        }

    def _generate_for_seeds(self, output_path, existing: set[str], seeds: list[QuestionSeed]) -> int:
        written = 0
        for seed in seeds:
            try:
                data, raw = self._request_questions(seed)
                if self.config.llm.save_raw_response:
                    save_raw_response(self.config.paths.raw_response_dir, f"generate_{seed.scope}_questions", seed.seed_chunk_id, raw)

                records = []
                for item in data if isinstance(data, list) else []:
                    question = str(item.get("question", "")).strip()
                    if not question or len(question) < 6:
                        continue
                    record = GeneratedQuestion(
                        id=stable_question_id(seed.scope, seed.seed_chunk_id, question),
                        question=question,
                        seed_chunk_id=seed.seed_chunk_id,
                        seed_chunk_ids=seed.seed_chunk_ids,
                        seed_source_file=seed.source_file,
                        question_scope=seed.scope,
                        doc_id=seed.doc_id,
                        doc_title=seed.doc_title,
                        section_title=seed.section_title,
                        section_path=seed.section_path,
                        question_type=item.get("question_type", "default"),
                        difficulty=item.get("difficulty", "medium"),
                        keywords=item.get("keywords", []),
                    )
                    if record.id in existing:
                        continue
                    existing.add(record.id)
                    records.append(record)
                if records:
                    append_jsonl(output_path, records)
                    written += len(records)
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, f"generate_{seed.scope}_questions", seed.raw_record, str(exc))
        return written

    def _request_questions(self, seed: QuestionSeed):
        allowed_types = ", ".join(self.config.question_generation.allowed_types)
        if seed.scope == "section":
            prompt = GENERATE_SECTION_QUESTIONS_USER.format(
                questions_per_item=self.config.question_generation.section_questions_per_item,
                allowed_types=allowed_types,
                doc_title=seed.doc_title,
                section_title=seed.section_title,
                section_path=seed.section_path,
                source_file=seed.source_file,
                content=seed.content,
            )
            system = GENERATE_SECTION_QUESTIONS_SYSTEM
        elif seed.scope == "document":
            prompt = GENERATE_DOCUMENT_QUESTIONS_USER.format(
                questions_per_item=self.config.question_generation.document_questions_per_item,
                allowed_types=allowed_types,
                doc_title=seed.doc_title,
                section_titles=seed.section_path,
                source_file=seed.source_file,
                content=seed.content,
            )
            system = GENERATE_DOCUMENT_QUESTIONS_SYSTEM
        else:
            prompt = GENERATE_QUESTIONS_USER.format(
                questions_per_chunk=self.config.question_generation.chunk_question_count,
                allowed_types=allowed_types,
                doc_title=seed.doc_title,
                section_title=seed.section_title,
                source_file=seed.source_file,
                content=seed.content,
            )
            system = GENERATE_QUESTIONS_SYSTEM

        return self.client.chat_json(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens,
        )
