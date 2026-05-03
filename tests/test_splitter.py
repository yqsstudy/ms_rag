"""Test document splitter"""

import pytest

from src.data.loader import Document
from src.data.splitter import Chunk, ChunkingConfig, DocumentSplitter


@pytest.fixture
def splitter():
    return DocumentSplitter()


@pytest.fixture
def sample_document():
    return Document(
        doc_id="test_doc",
        title="测试文档",
        content="# 概述\n\n这是概述内容。\n\n## 第一节\n\n第一节内容。\n\n## 第二节\n\n第二节内容。",
        source_url="https://example.com",
        file_path="/tmp/test.md",
    )


@pytest.fixture
def document_with_images():
    """文档包含图片"""
    return Document(
        doc_id="test_img_doc",
        title="测试图片文档",
        content="""# 概述

这是概述内容。

## 流程图

**图1** 详细排查流程图
![](images/test_flow.jpg)

**图2** 性能分析界面
![](images/test_screen.png)

## 其他内容

其他内容部分。
""",
        source_url="https://example.com",
        file_path="/tmp/test_img.md",
    )


def test_splitter_init(splitter):
    """Test splitter initialization"""
    assert splitter.config.min_chunk_size == 1500
    assert splitter.config.max_chunk_size == 2000


def test_split_document(splitter, sample_document):
    """Test splitting a document"""
    chunks = splitter.split_document(sample_document)

    assert len(chunks) > 0
    assert all(isinstance(chunk, Chunk) for chunk in chunks)


def test_chunk_metadata(splitter, sample_document):
    """Test chunk metadata"""
    chunks = splitter.split_document(sample_document)

    for chunk in chunks:
        assert chunk.chunk_id
        assert chunk.doc_id == sample_document.doc_id
        assert chunk.doc_title == sample_document.title
        assert chunk.source_url == sample_document.source_url


def test_chunk_to_dict(splitter, sample_document):
    """Test chunk to_dict method"""
    chunks = splitter.split_document(sample_document)

    for chunk in chunks:
        d = chunk.to_dict()
        assert isinstance(d, dict)
        assert "chunk_id" in d
        assert "content" in d
        assert "images" in d


def test_image_extraction(splitter, document_with_images):
    """Test image extraction"""
    chunks = splitter.split_document(document_with_images)

    # 找到包含图片的chunk
    img_chunk = None
    for chunk in chunks:
        if chunk.images:
            img_chunk = chunk
            break

    assert img_chunk is not None
    assert len(img_chunk.images) == 2

    # 验证图片信息
    img1 = img_chunk.images[0]
    assert img1["figure_num"] == "1"
    assert img1["caption"] == "详细排查流程图"
    assert img1["path"] == "images/test_flow.jpg"

    img2 = img_chunk.images[1]
    assert img2["figure_num"] == "2"
    assert img2["caption"] == "性能分析界面"


def test_custom_config():
    """Test custom chunking config"""
    config = ChunkingConfig(
        min_chunk_size=500,
        max_chunk_size=1000,
        chunk_overlap=100,
    )
    splitter = DocumentSplitter(config)

    assert splitter.config.min_chunk_size == 500
    assert splitter.config.max_chunk_size == 1000
