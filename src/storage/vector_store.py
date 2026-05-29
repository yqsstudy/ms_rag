"""Vector store using Chroma"""

import asyncio
import json
import logging
from pathlib import Path
from typing import List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from ..data.splitter import Chunk

logger = logging.getLogger("ms_rag")
MAX_CHROMA_BATCH_SIZE = 5000


class SearchResult:
    def __init__(
        self,
        chunk_id: str,
        content: str,
        metadata: dict,
        score: float,
    ):
        self.chunk_id = chunk_id
        self.content = content
        self.metadata = metadata
        self.score = score
        self.parent_id = metadata.get("parent_id", "")

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "metadata": self.metadata,
            "score": self.score,
            "parent_id": self.parent_id,
        }


class VectorStore:
    """Vector store wrapper for Chroma"""

    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        collection_name: str = "performance_guide",
    ):
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self._client: Optional[chromadb.Client] = None
        self._collection: Optional[chromadb.Collection] = None

    def _get_client(self) -> chromadb.Client:
        """Get or create Chroma client"""
        if self._client is None:
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        return self._client

    def _get_collection(self) -> chromadb.Collection:
        """Get or create collection"""
        if self._collection is None:
            client = self._get_client()
            self._collection = client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def add_chunks(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]],
    ) -> int:
        collection = self._get_collection()

        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [
            {
                "doc_id": chunk.doc_id,
                "doc_title": chunk.doc_title,
                "section_title": chunk.section_title,
                "source_url": chunk.source_url,
                "parent_topic": chunk.parent_topic or "",
                "images": json.dumps(chunk.images, ensure_ascii=False),
                "parent_id": chunk.parent_id or "",
            }
            for chunk in chunks
        ]

        for i in range(0, len(ids), MAX_CHROMA_BATCH_SIZE):
            collection.add(
                ids=ids[i:i + MAX_CHROMA_BATCH_SIZE],
                embeddings=embeddings[i:i + MAX_CHROMA_BATCH_SIZE],
                documents=documents[i:i + MAX_CHROMA_BATCH_SIZE],
                metadatas=metadatas[i:i + MAX_CHROMA_BATCH_SIZE],
            )

        return len(chunks)

    async def asearch(
        self,
        query_embedding: List[float],
        k: int = 10,
        where: Optional[dict] = None,
    ) -> List[SearchResult]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.search, query_embedding, k, where)

    def search(
        self,
        query_embedding: List[float],
        k: int = 10,
        where: Optional[dict] = None,
    ) -> List[SearchResult]:
        """Search for similar documents"""
        collection = self._get_collection()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        search_results = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                # Convert distance to similarity score (1 - distance for cosine)
                score = 1 - results["distances"][0][i] if results["distances"] else 0.0

                # 解析图片信息
                metadata = results["metadatas"][0][i]
                if "images" in metadata and isinstance(metadata["images"], str):
                    try:
                        metadata["images"] = json.loads(metadata["images"])
                    except json.JSONDecodeError:
                        metadata["images"] = []

                search_results.append(
                    SearchResult(
                        chunk_id=chunk_id,
                        content=results["documents"][0][i],
                        metadata=metadata,
                        score=score,
                    )
                )

        return search_results

    def delete_chunks(self, chunk_ids: List[str]) -> None:
        if not chunk_ids:
            return
        collection = self._get_collection()

        for i in range(0, len(chunk_ids), MAX_CHROMA_BATCH_SIZE):
            batch = chunk_ids[i:i + MAX_CHROMA_BATCH_SIZE]
            try:
                collection.delete(ids=batch)
            except Exception:
                logger.exception(
                    "[VectorStore] Failed to delete %s chunks from collection=%s",
                    len(batch),
                    self.collection_name,
                )
                raise

    def delete_all(self) -> None:
        """Delete all documents from collection"""
        client = self._get_client()
        try:
            client.delete_collection(self.collection_name)
            self._collection = None
        except Exception as exc:
            message = str(exc).lower()
            if "does not exist" in message or "not found" in message:
                logger.info("[VectorStore] Collection already absent: %s", self.collection_name)
                self._collection = None
                return
            logger.exception("[VectorStore] Failed to delete collection=%s", self.collection_name)
            raise

    def count(self) -> int:
        """Get number of documents in collection"""
        collection = self._get_collection()
        return collection.count()

    def get_chunk(self, chunk_id: str) -> Optional[dict]:
        """Get a specific chunk by ID"""
        collection = self._get_collection()
        results = collection.get(ids=[chunk_id], include=["documents", "metadatas"])
        if results["ids"]:
            metadata = results["metadatas"][0]
            # 解析图片信息
            if "images" in metadata and isinstance(metadata["images"], str):
                try:
                    metadata["images"] = json.loads(metadata["images"])
                except json.JSONDecodeError:
                    metadata["images"] = []

            return {
                "chunk_id": chunk_id,
                "content": results["documents"][0],
                "metadata": metadata,
            }
        return None