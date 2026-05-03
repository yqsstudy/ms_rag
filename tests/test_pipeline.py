"""Test RAG pipeline"""

import pytest

from src.core.config import Settings
from src.pipeline.rag_pipeline import RAGPipeline


@pytest.fixture
def settings():
    return Settings(
        embedding={"model": "BAAI/bge-large-zh", "device": "cpu"},
        vector_store={"persist_directory": "./data/chroma", "collection_name": "test"},
        llm={"provider": "anthropic", "model": "claude-sonnet-4-6"},
    )


@pytest.fixture
def pipeline(settings):
    return RAGPipeline(settings)


def test_pipeline_init(pipeline):
    """Test pipeline initialization"""
    assert pipeline.embedding_service is not None
    assert pipeline.vector_store is not None
    assert pipeline.keyword_index is not None
    assert pipeline.retriever is not None


def test_classify_question(pipeline):
    """Test question classification"""
    assert pipeline._classify_question("模型训练慢怎么定位？") == "定位指导"
    assert pipeline._classify_question("通信时间波动大是什么原因？") == "问题诊断"
    assert pipeline._classify_question("msprof怎么用？") == "工具使用"
    assert pipeline._classify_question("什么是快慢卡？") == "概念理解"
    assert pipeline._classify_question("如何查看通信耗时？") == "操作步骤"


def test_extract_keywords(pipeline):
    """Test keyword extraction"""
    keywords = pipeline._extract_keywords("msprof工具怎么分析通信问题？")

    assert "msprof" in keywords
    assert "通信" in keywords
