"""Test chunk overlap"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.loader import DocumentLoader
from src.data.splitter import ChunkingConfig, DocumentSplitter


def test_overlap():
    """Test overlap functionality"""
    # 创建测试文档
    test_content = """# 第一节

这是第一节的内容。包含一些文字描述。
这部分内容大约有几百字。
我们需要测试重叠功能是否正常工作。

# 第二节

这是第二节的内容。第二节和第一节之间应该有重叠。
重叠的内容可以帮助保持上下文连贯性。
这样检索时不会丢失边界信息。

# 第三节

这是第三节的内容。同样应该和第二节有重叠。
重叠策略可以避免信息在切分边界丢失。
这是一个重要的优化措施。
"""

    from src.data.loader import Document
    test_doc = Document(
        doc_id="test_overlap",
        title="测试重叠文档",
        content=test_content,
        source_url="https://example.com",
        file_path="/tmp/test.md",
    )

    # 使用较小的 chunk_size 方便测试
    config = ChunkingConfig(
        min_chunk_size=100,
        max_chunk_size=300,
        chunk_overlap=100,
    )
    splitter = DocumentSplitter(config)

    chunks = splitter.split_document(test_doc)

    print(f"文档切分成 {len(chunks)} 个 chunks")
    print(f"重叠大小: {config.chunk_overlap} 字符")
    print()

    for i, chunk in enumerate(chunks):
        print(f"=== Chunk {i}: {chunk.section_title} ===")
        print(f"长度: {len(chunk.content)} 字符")
        print(f"内容:\n{chunk.content[:200]}...")
        if i > 0:
            # 检查是否包含前一个 chunk 的结尾
            prev_chunk = chunks[i - 1]
            prev_end = prev_chunk.content[-50:]
            if prev_end in chunk.content:
                print(f"✅ 包含前一个 chunk 的结尾内容")
        if i < len(chunks) - 1:
            # 检查是否包含下一个 chunk 的开头
            next_chunk = chunks[i + 1]
            next_start = next_chunk.content[:50]
            if next_start in chunk.content:
                print(f"✅ 包含下一个 chunk 的开头内容")
        print()


def test_real_documents():
    """Test with real documents"""
    corpus_path = "./corpus/performance_guide"

    loader = DocumentLoader(corpus_path)
    documents = loader.load_all_documents()

    # 找一个较长的文档测试
    long_doc = None
    for doc in documents:
        if len(doc.content) > 3000:
            long_doc = doc
            break

    if long_doc:
        config = ChunkingConfig(
            min_chunk_size=500,
            max_chunk_size=1000,
            chunk_overlap=200,
        )
        splitter = DocumentSplitter(config)
        chunks = splitter.split_document(long_doc)

        print(f"\n测试真实文档: {long_doc.title}")
        print(f"原文长度: {len(long_doc.content)} 字符")
        print(f"切分成 {len(chunks)} 个 chunks")

        for i, chunk in enumerate(chunks[:3]):  # 只显示前3个
            print(f"\n=== Chunk {i}: {chunk.section_title} ===")
            print(f"长度: {len(chunk.content)} 字符")


if __name__ == "__main__":
    print("=" * 50)
    print("测试重叠功能")
    print("=" * 50)
    test_overlap()

    print("\n" + "=" * 50)
    print("测试真实文档")
    print("=" * 50)
    test_real_documents()