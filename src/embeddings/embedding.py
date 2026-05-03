"""Embedding service using sentence-transformers"""

from typing import List, Optional

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Embedding service for text vectorization"""

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-zh",
        device: str = "cpu",
        normalize: bool = True,
    ):
        self.model_name = model_name
        self.device = device
        self.normalize = normalize
        self._model: Optional[SentenceTransformer] = None

    def _load_model(self) -> SentenceTransformer:
        """Load embedding model (lazy loading)"""
        if self._model is None:
            self._model = SentenceTransformer(
                self.model_name,
                device=self.device,
            )
        return self._model

    def embed_texts(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Embed a list of texts"""
        model = self._load_model()
        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=self.normalize,
            show_progress_bar=len(texts) > 100,
        )
        return [emb.tolist() for emb in embeddings]

    def embed_query(self, query: str) -> List[float]:
        """Embed a single query"""
        model = self._load_model()
        embedding = model.encode(
            query,
            normalize_embeddings=self.normalize,
        )
        return embedding.tolist()

    def get_embedding_dimension(self) -> int:
        """Get embedding dimension"""
        model = self._load_model()
        return model.get_sentence_embedding_dimension()

    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._model is not None