"""Test vector store reliability behavior."""

import pytest

from src.storage.vector_store import VectorStore


class FailingCollection:
    def delete(self, ids):
        raise RuntimeError(f"delete failed for {ids}")


class MissingCollectionClient:
    def delete_collection(self, name):
        raise RuntimeError(f"Collection {name} does not exist")


class FailingClient:
    def delete_collection(self, name):
        raise RuntimeError("disk unavailable")


def test_delete_chunks_reraises_delete_failures():
    store = VectorStore(collection_name="test")
    store._collection = FailingCollection()

    with pytest.raises(RuntimeError, match="delete failed"):
        store.delete_chunks(["chunk-1"])


def test_delete_all_ignores_missing_collection():
    store = VectorStore(collection_name="missing")
    store._client = MissingCollectionClient()
    store._collection = object()

    store.delete_all()

    assert store._collection is None


def test_delete_all_reraises_unexpected_failures():
    store = VectorStore(collection_name="test")
    store._client = FailingClient()

    with pytest.raises(RuntimeError, match="disk unavailable"):
        store.delete_all()
