"""Synthesize final eval samples from judged supporting evidence."""

from __future__ import annotations

import hashlib
import json

from .chunk_source import ChunkSource
from .config import RagEvalConfig
from .io import append_jsonl, load_existing_ids, read_jsonl, save_raw_response, write_failed_record, write_jsonl
from .openai_client import OpenAICompatibleClient
from .prompt_templates import SYNTHESIZE_ANSWER_SYSTEM, SYNTHESIZE_ANSWER_USER
from .schemas import AnswerKeyPoint, EvalSample, EvidenceJudgment, GeneratedQuestion


def stable_eval_id(question: str, chunk_ids: list[str]) -> str:
    digest = hashlib.sha1(f"{question}:{','.join(sorted(chunk_ids))}".encode("utf-8")).hexdigest()[:12]
    return f"eval_{digest}"


class AnswerSynthesizer:
    def __init__(self, config: RagEvalConfig, client: OpenAICompatibleClient):
        self.config = config
        self.client = client
        self.chunk_source = ChunkSource(config)
        self.questions = {
            item.id: item
            for item in read_jsonl(self.config.output_dir / "questions.jsonl", GeneratedQuestion)
        }

    def synthesize(self, limit: int | None = None, offset: int = 0, force: bool = False) -> int:
        input_path = self.config.output_dir / "evidence_judgments.jsonl"
        output_path = self.config.output_dir / "eval_dataset_draft.jsonl"
        if force:
            write_jsonl(output_path, [])
        existing = set() if force else load_existing_ids(output_path, "question_id")
        existing_questions = set()
        if not force:
            existing_questions = {
                str(item.get("question"))
                for item in read_jsonl(output_path)
                if item.get("question")
            }
        judgments = read_jsonl(input_path, EvidenceJudgment)[offset:]
        if limit:
            judgments = judgments[:limit]
        written = 0
        for judgment in judgments:
            if judgment.question_id in existing or judgment.question in existing_questions:
                continue
            try:
                sample = self._synthesize_one(judgment)
                append_jsonl(output_path, [sample])
                existing.add(judgment.question_id)
                existing_questions.add(judgment.question)
                written += 1
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, "synthesize_answers", judgment.model_dump(), str(exc))
        return written

    def _synthesize_one(self, judgment: EvidenceJudgment) -> EvalSample:
        selected_ids = [
            item.chunk_id for item in judgment.judged_chunks
            if item.relevance >= self.config.llm_judge.relevance_threshold
        ][: self.config.synthesis.max_supporting_chunks]
        question_meta = self.questions.get(judgment.question_id)
        chunks = []
        for chunk_id in selected_ids:
            chunk = self.chunk_source.get(chunk_id)
            if not chunk:
                continue
            chunks.append({
                "chunk_id": chunk.chunk_id,
                "source_file": chunk.source_file,
                "section_path": chunk.section_path,
                "content": chunk.content[: self.config.synthesis.max_chunk_chars],
            })

        prompt = SYNTHESIZE_ANSWER_USER.format(
            question=judgment.question,
            question_type=question_meta.question_type if question_meta else "default",
            difficulty=question_meta.difficulty if question_meta else "medium",
            keywords=json.dumps(question_meta.keywords if question_meta else [], ensure_ascii=False),
            chunks_json=json.dumps(chunks, ensure_ascii=False, indent=2),
            max_must_have_points=self.config.synthesis.max_must_have_points,
            max_nice_to_have_points=self.config.synthesis.max_nice_to_have_points,
        )
        data, raw = self.client.chat_json(
            [
                {"role": "system", "content": SYNTHESIZE_ANSWER_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens,
        )
        if self.config.llm.save_raw_response:
            save_raw_response(self.config.paths.raw_response_dir, "synthesize_answers", judgment.question_id, raw)

        acceptable_chunk_ids = data.get("acceptable_chunk_ids", selected_ids) if isinstance(data, dict) else selected_ids
        return EvalSample(
            id=stable_eval_id(judgment.question, acceptable_chunk_ids),
            question_id=judgment.question_id,
            question=judgment.question,
            question_type=question_meta.question_type if question_meta else "default",
            difficulty=question_meta.difficulty if question_meta else "medium",
            question_scope=question_meta.question_scope if question_meta else "chunk",
            doc_id=question_meta.doc_id if question_meta else "",
            doc_title=question_meta.doc_title if question_meta else "",
            section_title=question_meta.section_title if question_meta else "",
            section_path=question_meta.section_path if question_meta else "",
            answer_key_points=[AnswerKeyPoint.model_validate(item) for item in data.get("answer_key_points", [])],
            must_have_points=data.get("must_have_points", []),
            nice_to_have_points=data.get("nice_to_have_points", []),
            expected_answer=data.get("expected_answer", ""),
            acceptable_chunk_ids=acceptable_chunk_ids,
            acceptable_source_files=data.get("acceptable_source_files", []),
            keywords=question_meta.keywords if question_meta else [],
            is_answerable=bool(data.get("is_answerable", bool(selected_ids))),
            conflicts=data.get("conflicts", []),
        )
