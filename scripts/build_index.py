"""Build index script"""

import argparse
import json
import logging
import re
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
from src.storage.document_store import DocumentStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _build_graph(documents, chunks) -> dict:
    parent_map = {}
    children_map = {}
    doc_chunks_map = {}
    doc_titles = {}
    references = {}

    stem_to_doc_id = {Path(doc.file_path).stem: doc.doc_id for doc in documents}

    for doc in documents:
        doc_id = doc.doc_id
        doc_titles[doc_id] = doc.title

        if doc.parent_topic:
            parent_id = stem_to_doc_id.get(doc.parent_topic, doc.parent_topic)
            parent_map[doc_id] = parent_id
            children_map.setdefault(parent_id, [])
            if doc_id not in children_map[parent_id]:
                children_map[parent_id].append(doc_id)

    for chunk in chunks:
        doc_id = chunk.doc_id
        doc_chunks_map.setdefault(doc_id, [])
        if chunk.chunk_id not in doc_chunks_map[doc_id]:
            doc_chunks_map[doc_id].append(chunk.chunk_id)

    ref_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for doc in documents:
        matches = ref_pattern.findall(doc.content)
        if matches:
            refs = set()
            for m in matches:
                url = m[1]
                if url.startswith(("http://", "https://")):
                    continue
                doc_id_match = re.search(r"([^/]+)(?:\.md|\.html)$", url)
                if doc_id_match:
                    stem = doc_id_match.group(1).replace(".md", "").replace(".html", "")
                    refs.add(stem_to_doc_id.get(stem, stem))
                elif "toolsample" in url or "sample" in url:
                    doc_id_match = re.search(r"((?:toolsample|sample)\d+(?:_\d+)?)", url)
                    if doc_id_match:
                        stem = doc_id_match.group(1)
                        refs.add(stem_to_doc_id.get(stem, stem))
            if refs:
                references[doc.doc_id] = list(refs)

    return {
        "parent_map": parent_map,
        "children_map": children_map,
        "doc_chunks_map": doc_chunks_map,
        "doc_titles": doc_titles,
        "references": references,
    }


def build_index(
    corpus_path: str,
    persist_directory: str,
    collection_name: str,
    batch_size: int = 32,
    force_rebuild: bool = False,
):
    logger.info(f"Loading documents from {corpus_path}")

    loader = DocumentLoader(corpus_path)
    documents = loader.load_all_documents()
    logger.info(f"Loaded {len(documents)} documents")

    state_path = Path(persist_directory).parent / "index_state.json"
    index_state = {}
    if not force_rebuild and state_path.exists():
        try:
            with open(state_path, "r", encoding="utf-8") as f:
                index_state = json.load(f)
            logger.info(f"Loaded previous index state with {len(index_state)} entries")
        except json.JSONDecodeError:
            logger.warning("Failed to parse index_state.json, will rebuild all")
    
    docs_to_process = []
    docs_unchanged = 0
    docs_modified = 0
    docs_new = 0

    current_files = set()

    for doc in documents:
        current_files.add(doc.file_path)
        file_hash = getattr(doc, 'file_hash', None)
        state_entry = index_state.get(doc.file_path)

        if not force_rebuild and state_entry and state_entry.get("hash") == file_hash:
            docs_unchanged += 1
            continue

        if state_entry:
            docs_modified += 1
        else:
            docs_new += 1
            
        docs_to_process.append(doc)

    deleted_files = set(index_state.keys()) - current_files
    
    logger.info(f"Docs summary: {docs_unchanged} unchanged, {docs_modified} modified, {docs_new} new, {len(deleted_files)} deleted")

    if not force_rebuild and not docs_to_process and not deleted_files:
        logger.info("No changes detected in corpus. Index is up to date.")
        return {
            "documents": len(documents),
            "parent_chunks": 0,
            "child_chunks": 0,
            "vector_store_count": 0,
            "bm25_count": 0,
        }

    doc_store_path = Path(persist_directory).parent / "docstore"
    doc_store = DocumentStore(persist_directory=str(doc_store_path))
    
    vector_store = VectorStore(
        persist_directory=persist_directory,
        collection_name=collection_name,
    )

    if force_rebuild:
        doc_store.delete_all()
        vector_store.delete_all()
        index_state = {}
        logger.info("Cleared existing stores for full rebuild")
    else:
        files_to_delete = list(deleted_files) + [doc.file_path for doc in docs_to_process if doc.file_path in index_state]
        
        parent_ids_to_delete = []
        child_ids_to_delete = []
        
        for file_path in files_to_delete:
            entry = index_state.get(file_path, {})
            parent_ids_to_delete.extend(entry.get("parent_chunks", []))
            child_ids_to_delete.extend(entry.get("child_chunks", []))
            if file_path in index_state:
                del index_state[file_path]
                
        if parent_ids_to_delete:
            logger.info(f"Removing {len(parent_ids_to_delete)} old parent chunks")
            doc_store.delete_documents(parent_ids_to_delete)
            
        if child_ids_to_delete:
            logger.info(f"Removing {len(child_ids_to_delete)} old child chunks")
            vector_store.delete_chunks(child_ids_to_delete)

    cleaner = TextCleaner()
    splitter = DocumentSplitter()

    all_chunks = []
    child_chunks = []
    
    for doc in docs_to_process:
        cleaned_content = cleaner.clean_chunk_content(doc.content)
        doc.content = cleaned_content

        parent_chunks = splitter.split_document(doc)
        all_chunks.extend(parent_chunks)
        
        doc_child_chunks = []
        for parent in parent_chunks:
            children = splitter.split_into_children(parent)
            doc_child_chunks.extend(children)
            child_chunks.extend(children)
            
        index_state[doc.file_path] = {
            "hash": getattr(doc, 'file_hash', None),
            "parent_chunks": [p.chunk_id for p in parent_chunks],
            "child_chunks": [c.chunk_id for c in doc_child_chunks]
        }

    if all_chunks:
        logger.info(f"Created {len(all_chunks)} parent chunks and {len(child_chunks)} child chunks")

        doc_dicts = {c.chunk_id: c.to_dict() for c in all_chunks}
        doc_store.add_documents(doc_dicts)
        logger.info(f"Stored {len(all_chunks)} parent chunks")

        logger.info("Generating embeddings for child chunks...")
        embedding_service = EmbeddingService()
        embeddings = embedding_service.embed_texts(
            [c.content for c in child_chunks],
            batch_size=batch_size,
        )
        logger.info(f"Generated {len(embeddings)} embeddings")

        vector_store.add_chunks(child_chunks, embeddings)
        logger.info(f"Stored {len(child_chunks)} child chunks in vector store")

    logger.info("Rebuilding BM25 index...")
    active_child_chunks = []
    if not force_rebuild and (docs_unchanged > 0 or deleted_files):
        logger.warning("BM25 incremental update not fully supported, rebuilding from all vectors...")
        for doc in documents:
            if doc.file_path not in deleted_files:
                doc.content = cleaner.clean_chunk_content(doc.content)
                parent_chunks = splitter.split_document(doc)
                for parent in parent_chunks:
                    active_child_chunks.extend(splitter.split_into_children(parent))
    else:
        active_child_chunks = child_chunks

    bm25_index = BM25Index()
    bm25_index.build_index(active_child_chunks)
    bm25_index.save()
    logger.info(f"Built BM25 index with {bm25_index.count()} documents")

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(index_state, f, ensure_ascii=False, indent=2)

    logger.info("Building knowledge graph...")
    valid_documents = [d for d in documents if d.file_path not in deleted_files]
    valid_parents = []
    for doc in valid_documents:
        doc.content = cleaner.clean_chunk_content(doc.content)
        valid_parents.extend(splitter.split_document(doc))
        
    graph = _build_graph(valid_documents, valid_parents)
    graph_path = Path(persist_directory).parent / "graph.json"
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved knowledge graph to {graph_path}")

    logger.info("Index build complete!")

    return {
        "documents": len(valid_documents),
        "parent_chunks": len(all_chunks),
        "child_chunks": len(child_chunks),
        "vector_store_count": vector_store.count(),
        "bm25_count": bm25_index.count(),
    }


def main():
    parser = argparse.ArgumentParser(description="Build RAG index")
    parser.add_argument(
        "--corpus",
        default="./corpus",
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
    print(f"  Parent Chunks: {result['parent_chunks']}")
    print(f"  Child Chunks: {result['child_chunks']}")
    print(f"  Vector store: {result['vector_store_count']}")
    print(f"  BM25 index: {result['bm25_count']}")


if __name__ == "__main__":
    main()