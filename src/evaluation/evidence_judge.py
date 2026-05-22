"""LLM-based evidence relevance judging."""

from __future__ import annotations

import json

from .config import RagEvalConfig
from .io import append_jsonl, read_jsonl, save_raw_response, write_failed_record
from .openai_client import OpenAICompatibleClient
from .prompt_templates import JUDGE_EVIDENCE_SYSTEM, JUDGE_EVIDENCE_USER
from .schemas import EvidenceCardSet, EvidenceJudgment, JudgedChunk


class EvidenceJudge:
    def __init__(self, config: RagEvalConfig, client: OpenAICompatibleClient):
        self.config = config
        self.client = client

    def judge(self, limit: int | None = None, offset: int = 0) -> int:
        input_path = self.config.output_dir / "evidence_cards.jsonl"
        output_path = self.config.output_dir / "evidence_judgments.jsonl"
        card_sets = read_jsonl(input_path, EvidenceCardSet)[offset:]
        if limit:
            card_sets = card_sets[:limit]
        written = 0
        for card_set in card_sets:
            try:
                judgment = self._judge_one(card_set)
                append_jsonl(output_path, [judgment])
                written += 1
            except Exception as exc:  # noqa: BLE001
                write_failed_record(self.config.output_dir, "judge_evidence", card_set.model_dump(), str(exc))
        return written

    def _judge_one(self, card_set: EvidenceCardSet) -> EvidenceJudgment:
        cards = [card.model_dump(mode="json") for card in card_set.cards]
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
            save_raw_response(self.config.paths.raw_response_dir, "judge_evidence", card_set.question_id, raw)
        judged = []
        for item in data.get("judged_chunks", []) if isinstance(data, dict) else []:
            judged.append(JudgedChunk.model_validate(item))
        return EvidenceJudgment(
            question_id=card_set.question_id,
            question=card_set.question,
            judged_chunks=judged,
        )
