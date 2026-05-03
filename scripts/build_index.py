"""Build index script"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.config import get_settings
from src.data.cleaner import TextCleaner
from src.data.loader import DocumentLoader
from src.data.splitter import ChunkingConfig, DocumentSplitter
from src.embeddings.embedding import EmbeddingService
from src.storage.keyword_index import BM25Index
from src.storage.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_index(
    corpus_path: str,
    persist_directory: str,
    collection_name: str,
    batch_size: int = 32,
    force_rebuild: bool = False,
):
    """Build vector and keyword indexes from corpus"""
    logger.info(f"Loading documents from {corpus_path}")

    # 1. Load documents
    loader = DocumentLoader(corpus_path)
    documents = loader.load_all_documents()
    logger.info(f"Loaded {len(documents)} documents")

    # 2. Clean and split documents
    cleaner = TextCleaner()
    splitter = DocumentSplitter()

    all_chunks = []
    for doc in documents:
        # Clean content
        cleaned_content = cleaner.clean_chunk_content(doc.content)
        doc.content = cleaned_content

        # Split into chunks
        chunks = splitter.split_document(doc)
        all_chunks.extend(chunks)

    logger.info(f"Created {len(all_chunks)} chunks")

    # 3. Generate embeddings
    logger.info("Generating embeddings...")
    embedding_service = EmbeddingService()
    embeddings = embedding_service.embed_texts(
        [c.content for c in all_chunks],
        batch_size=batch_size,
    )
    logger.info(f"Generated {len(embeddings)} embeddings")

    # 4. Store in vector database
    logger.info("Storing in vector database...")
    vector_store = VectorStore(
        persist_directory=persist_directory,
        collection_name=collection_name,
    )

    if force_rebuild:
        vector_store.delete_all()
        logger.info("Cleared existing index")

    vector_store.add_chunks(all_chunks, embeddings)
    logger.info(f"Stored {vector_store.count()} chunks in vector store")

    # 5. Build BM25 index
    logger.info("Building BM25 index...")
    bm25_index = BM25Index()
    bm25_index.build_index(all_chunks)
    bm25_index.save()
    logger.info(f"Built BM25 index with {bm25_index.count()} documents")

    logger.info("Index build complete!")

    return {
        "documents": len(documents),
        "chunks": len(all_chunks),
        "vector_store_count": vector_store.count(),
        "bm25_count": bm25_index.count(),
    }


def main():
    parser = argparse.ArgumentParser(description="Build RAG index")
    parser.add_argument(
        "--corpus",
        default="./corpus/performance_guide",
        help="Path to corpus directory",
    )
    parser.add_argument(
        "--output",
        default="./data/chroma",
        help="Output directory for vector store",
    )
    parser.add_argument(
        "--collection",
        default="performance_guide",
        help="Collection name",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for embedding",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild index",
    )
    parser.add_argument(
        "--config",
        default="./config/system.yaml",
        help="Path to config file",
    )

    args = parser.parse_args()

    # Load settings if config exists
    config_path = Path(args.config)
    if config_path.exists():
        settings = get_settings(args.config)
        corpus_path = settings.corpus_path
        persist_directory = settings.vector_store.persist_directory
        collection_name = settings.vector_store.collection_name
        batch_size = settings.embedding.batch_size
    else:
        corpus_path = args.corpus
        persist_directory = args.output
        collection_name = args.collection
        batch_size = args.batch_size

    result = build_index(
        corpus_path=corpus_path,
        persist_directory=persist_directory,
        collection_name=collection_name,
        batch_size=batch_size,
        force_rebuild=args.force,
    )

    print(f"\nIndex build summary:")
    print(f"  Documents: {result['documents']}")
    print(f"  Chunks: {result['chunks']}")
    print(f"  Vector store: {result['vector_store_count']}")
    print(f"  BM25 index: {result['bm25_count']}")


if __name__ == "__main__":
    main()