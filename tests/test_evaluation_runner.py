"""Test retrieval evaluation release gates."""

import pytest

from src.evaluation.config import RagEvalConfig
from src.evaluation.runner import EvaluationThresholdError, RetrievalEvaluationRunner


def make_runner(fail_under):
    runner = RetrievalEvaluationRunner.__new__(RetrievalEvaluationRunner)
    runner.config = RagEvalConfig.model_validate({"evaluation": {"fail_under": fail_under}})
    return runner


def test_check_thresholds_accepts_metrics_at_threshold():
    runner = make_runner({"mrr": 0.8, "hit@5": 0.9})

    runner._check_thresholds({"mrr": 0.8, "hit@5": 0.95})


def test_check_thresholds_rejects_metrics_below_threshold():
    runner = make_runner({"mrr": 0.8})

    with pytest.raises(EvaluationThresholdError, match="mrr=0.7000 < 0.8000"):
        runner._check_thresholds({"mrr": 0.7})


def test_check_thresholds_rejects_missing_metrics():
    runner = make_runner({"hit@10": 0.9})

    with pytest.raises(EvaluationThresholdError, match="hit@10 is missing"):
        runner._check_thresholds({"mrr": 1.0})
