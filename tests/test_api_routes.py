"""Test API route hardening."""

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.api.routes import get_pipeline, internal_error, require_admin


class FakeRequest:
    def __init__(self, pipeline=None, admin_token=None, headers=None):
        self.app = SimpleNamespace(
            state=SimpleNamespace(
                pipeline=pipeline,
                settings=SimpleNamespace(api=SimpleNamespace(admin_token=admin_token)),
            )
        )
        self.headers = headers or {}


def test_get_pipeline_returns_app_state_pipeline():
    pipeline = object()

    assert get_pipeline(FakeRequest(pipeline=pipeline)) is pipeline


def test_get_pipeline_reports_not_ready_without_lazy_global_init():
    with pytest.raises(HTTPException) as exc_info:
        get_pipeline(FakeRequest(pipeline=None))

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "RAG pipeline is not ready"


def test_require_admin_rejects_disabled_admin_api():
    with pytest.raises(HTTPException) as exc_info:
        require_admin(FakeRequest(admin_token=None))

    assert exc_info.value.status_code == 403


def test_require_admin_rejects_invalid_token():
    request = FakeRequest(admin_token="secret", headers={"x-admin-token": "wrong"})

    with pytest.raises(HTTPException) as exc_info:
        require_admin(request)

    assert exc_info.value.status_code == 403


def test_require_admin_accepts_valid_token():
    request = FakeRequest(admin_token="secret", headers={"x-admin-token": "secret"})

    assert require_admin(request) is None


def test_internal_error_uses_stable_public_message():
    error = internal_error("QA", RuntimeError("database password leaked in exception"))

    assert error.status_code == 500
    assert error.detail == "Internal server error"
