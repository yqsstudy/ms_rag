"""Test document loader"""

from pathlib import Path

import pytest

from src.data.loader import Document, DocumentLoader


@pytest.fixture
def corpus_path():
    return Path("./corpus/performance_guide")


@pytest.fixture
def loader(corpus_path):
    return DocumentLoader(str(corpus_path))


def test_loader_init(loader):
    """Test loader initialization"""
    assert loader.corpus_path.exists()


def test_load_all_documents(loader):
    """Test loading all documents"""
    documents = loader.load_all_documents()

    assert len(documents) > 0
    assert all(isinstance(doc, Document) for doc in documents)


def test_document_fields(loader):
    """Test document fields are populated"""
    documents = loader.load_all_documents()

    for doc in documents:
        assert doc.doc_id
        assert doc.title
        assert doc.content
        assert doc.source_url


def test_get_document_count(loader):
    """Test document count"""
    count = loader.get_document_count()
    assert count > 0
    assert count == len(loader.load_all_documents())
