"""LLM-based evidence relevance judging."""

from __future__ import annotations

import json

from .config import RagEvalConfig
from .io import append_jsonl, load_existing_ids, read_jsonl, save_raw_response, write_failed_record, write_jsonl
from .openai_client import OpenAICompatibleClient
from .prompt_templates import JUDGE_EVIDENCE_SYSTEM, JUDGE_EVIDENCE_USER
from .schemas import EvidenceCardSet, EvidenceJudgment, JudgedChunk


class EvidenceJudge:
    def __init__(self, config: RagEvalConfig, client: OpenAICompatibleClient):
        self.config = config
        self.client = client

    def judge(self, limit: int | None = None, offset: int = 0, force: bool = False) -> int:
        input_path = self.config.output_dir / "evidence_cards.jsonl"
        output_path = self.config.output_dir / "evidence_judgments.jsonl"
        if force:
            write_jsonl(output_path, [])
        existing = set() if force else load_existing_ids(output_path, "question_id")
        card_sets = read_jsonl(input_path, EvidenceCardSet)[offset:]
        if limit:
            card_sets = card_sets[:limit]
        written = 0
        for card_set in card_sets:
            if card_set.question_id in existing:
                continue
            try:
                judgment = self._judge_one(card_set)
                append_jsonl(output_path, [judgment])
                existing.add(card_set.question_id)
                written += 1
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, "judge_evidence", card_set.model_dump(), str(exc))
        return written

    def _judge_one(self, card_set: EvidenceCardSet) -> EvidenceJudgment:
        judged_by_chunk: dict[str, JudgedChunk] = {}
        cards = [card.model_dump(mode="json") for card in card_set.cards]
        cards_per_request = max(1, self.config.llm_judge.cards_per_request)
        for batch_index, start in enumerate(range(0, len(cards), cards_per_request), start=1):
            batch = cards[start:start + cards_per_request]
            batch_judged = self._judge_batch(card_set, batch, batch_index)
            for item in batch_judged:
                existing = judged_by_chunk.get(item.chunk_id)
                if not existing or item.relevance > existing.relevance:
                    judged_by_chunk[item.chunk_id] = item
                elif item.relevance == existing.relevance:
                    existing.supported_points = list(dict.fromkeys(existing.supported_points + item.supported_points))
                    if item.reason and item.reason not in existing.reason:
                        existing.reason = f"{existing.reason}; {item.reason}" if existing.reason else item.reason
        return EvidenceJudgment(
            question_id=card_set.question_id,
            question=card_set.question,
            judged_chunks=list(judged_by_chunk.values()),
        )

    def _judge_batch(self, card_set: EvidenceCardSet, cards: list[dict], batch_index: int) -> list[JudgedChunk]:
        prompt = JUDGE_EVIDENCE_USER.format(
            question=card_set.question,
            cards_json=json.dumps(cards, ensure_ascii=False, indent=2),
        )
        data, raw = self.client.chat_json(
            [
                {"role": "system", "content": JUDGE_EVIDENCE_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens,
        )
        if self.config.llm.save_raw_response:
            save_raw_response(
                self.config.paths.raw_response_dir,
                "judge_evidence",
                f"{card_set.question_id}_batch_{batch_index}",
                raw,
            )
        return [
            JudgedChunk.model_validate(item)
            for item in data.get("judged_chunks", [])
        ] if isinstance(data, dict) else []
