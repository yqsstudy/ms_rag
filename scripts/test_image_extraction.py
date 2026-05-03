"""Test image extraction"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.loader import DocumentLoader
from src.data.splitter import DocumentSplitter


def test_image_extraction():
    """Test image extraction from documents"""
    corpus_path = "./corpus/performance_guide"

    # Load documents
    loader = DocumentLoader(corpus_path)
    documents = loader.load_all_documents()
    print(f"Loaded {len(documents)} documents")

    # Split documents
    splitter = DocumentSplitter()

    total_images = 0
    docs_with_images = []

    for doc in documents:
        chunks = splitter.split_document(doc)

        for chunk in chunks:
            if chunk.images:
                total_images += len(chunk.images)
                if doc.doc_id not in docs_with_images:
                    docs_with_images.append(doc.doc_id)
                    print(f"\n文档: {doc.title} ({doc.doc_id})")
                    print(f"  章节: {chunk.section_title}")
                    for img in chunk.images:
                        if img.get("figure_num"):
                            print(f"    图{img['figure_num']}: {img.get('caption', '未命名')}")
                        else:
                            print(f"    图片: {img.get('caption', '未命名')}")

    print(f"\n统计:")
    print(f"  包含图片的文档数: {len(docs_with_images)}")
    print(f"  提取的图片总数: {total_images}")


if __name__ == "__main__":
    test_image_extraction()
