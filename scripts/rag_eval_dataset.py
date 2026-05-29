"""Offline RAG eval dataset generation CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.evaluation.config import RagEvalConfig, load_eval_config
from src.evaluation.openai_client import OpenAICompatibleClient


def build_client(config: RagEvalConfig) -> OpenAICompatibleClient:
    return OpenAICompatibleClient(
        base_url=config.llm.base_url,
        api_key=config.llm.api_key,
        model=config.llm.model,
        timeout_seconds=config.llm.timeout_seconds,
        max_retries=config.llm.max_retries,
        retry_backoff_seconds=config.llm.retry_backoff_seconds,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and evaluate RAG eval datasets")
    parser.add_argument("command", choices=[
        "generate-questions",
        "build-evidence-pool",
        "build-evidence-cards",
        "judge-evidence",
        "synthesize-answers",
        "finalize-dataset",
        "evaluate",
        "report",
    ])
    parser.add_argument("--config", default="config/rag_eval.yaml")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    config = load_eval_config(args.config)
    config.output_dir.mkdir(parents=True, exist_ok=True)

    if args.command == "generate-questions":
        from src.evaluation.question_generator import QuestionGenerator

        count = QuestionGenerator(config, build_client(config)).generate(args.limit, args.offset, args.force)
        print(f"Generated {count} questions")
    elif args.command == "build-evidence-pool":
        from src.evaluation.evidence_pool import EvidencePoolBuilder

        count = EvidencePoolBuilder(config).build(args.limit, args.offset, args.force)
        print(f"Built {count} candidate pools")
    elif args.command == "build-evidence-cards":
        from src.evaluation.evidence_cards import EvidenceCardBuilder

        count = EvidenceCardBuilder(config).build(args.limit, args.offset, args.force)
        print(f"Built {count} evidence card sets")
    elif args.command == "judge-evidence":
        from src.evaluation.evidence_judge import EvidenceJudge

        count = EvidenceJudge(config, build_client(config)).judge(args.limit, args.offset, args.force)
        print(f"Judged {count} evidence card sets")
    elif args.command == "synthesize-answers":
        from src.evaluation.answer_synthesizer import AnswerSynthesizer

        count = AnswerSynthesizer(config, build_client(config)).synthesize(args.limit, args.offset, args.force)
        print(f"Synthesized {count} eval samples")
    elif args.command == "finalize-dataset":
        from src.evaluation.dataset_finalizer import DatasetFinalizer

        count = DatasetFinalizer(config).finalize()
        print(f"Finalized {count} eval samples")
    elif args.command == "evaluate":
        from src.evaluation.runner import RetrievalEvaluationRunner

        run_dir = RetrievalEvaluationRunner(config).run(args.limit, args.offset)
        print(f"Evaluation run saved to: {run_dir}")
    elif args.command == "report":
        from src.evaluation.reporter import ReportWriter

        report_path = ReportWriter(config).write_latest()
        print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
