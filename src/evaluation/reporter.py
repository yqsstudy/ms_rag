"""Markdown report generation for RAG eval runs."""

from __future__ import annotations

import json
from pathlib import Path

from .config import RagEvalConfig
from .io import read_jsonl


class ReportWriter:
    def __init__(self, config: RagEvalConfig):
        self.config = config

    def write_latest(self) -> Path:
        runs_dir = self.config.output_dir / "runs"
        if not runs_dir.exists():
            raise FileNotFoundError("No eval runs found")
        run_dirs = sorted([path for path in runs_dir.iterdir() if path.is_dir()])
        if not run_dirs:
            raise FileNotFoundError("No eval runs found")
        return self.write(run_dirs[-1])

    def write(self, run_dir: str | Path) -> Path:
        run_path = Path(run_dir)
        summaries = read_jsonl(run_path / "metrics.jsonl")
        if not summaries:
            raise FileNotFoundError(f"No metrics found in {run_path}")
        summary = summaries[0]
        report_path = run_path / "report.md"
        lines = [
            "# RAG Retrieval Evaluation Report",
            "",
            f"Run: `{run_path.name}`",
            f"Cases: {summary.get('num_cases', 0)}",
            "",
            "## Retrieval Metrics",
            "",
            "| Metric | Value |",
            "|---|---:|",
        ]
        for key, value in summary.get("retrieval", {}).items():
            lines.append(f"| {key} | {value:.4f} |")
        lines.extend([
            "",
            "## Latency",
            "",
            "| Metric | Value |",
            "|---|---:|",
        ])
        for key, value in summary.get("latency", {}).items():
            lines.append(f"| {key} | {value:.2f} ms |")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return report_path
