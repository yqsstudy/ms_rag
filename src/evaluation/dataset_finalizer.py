"""Finalize evaluation datasets."""

from __future__ import annotations

from .config import RagEvalConfig
from .io import read_jsonl, write_jsonl
from .schemas import EvalSample


class DatasetFinalizer:
    def __init__(self, config: RagEvalConfig):
        self.config = config

    def finalize(self) -> int:
        draft_path = self.config.output_dir / "eval_dataset_draft.jsonl"
        output_path = self.config.output_dir / "eval_dataset.jsonl"
        samples = read_jsonl(draft_path, EvalSample)
        final_samples = [
            sample for sample in samples
            if sample.is_answerable and sample.acceptable_chunk_ids
        ]
        write_jsonl(output_path, final_samples)
        return len(final_samples)
