"""RAG Pipeline"""

import logging
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator, List, Optional, Any

from ..cache.cache_manager import CacheManager
from ..core.config import Settings
from ..core.tracing import tracer
from ..embeddings.embedding import EmbeddingService
from ..generation.context_builder import ContextBuilder
from ..generation.llm_service import LLMService
from ..generation.prompt_templates import PromptTemplateManager
from ..retrieval.hybrid_retriever import HybridRetriever, HybridResult
from ..retrieval.kg_enhancer import KnowledgeGraphEnhancer
from ..retrieval.reranker import Reranker
from ..storage.keyword_index import BM25Index
from ..storage.vector_store import VectorStore
from ..storage.document_store import DocumentStore

logger = logging.getLogger("ms_rag")


@dataclass
class QAResponse:
    """QA response"""

    answer: str
    sources: List[dict]
    question_type: str
    keywords: List[str]
    metadata: dict


class RAGPipeline:
    """RAG pipeline for question answering"""

    def __init__(self, settings: Settings):
        self.settings = settings

        # Initialize components
        self.embedding_service = EmbeddingService(
            model_name=settings.embedding.model,
            device=settings.embedding.device,
            normalize=settings.embedding.normalize,
        )

        self.vector_store = VectorStore(
            persist_directory=settings.vector_store.persist_directory,
            collection_name=settings.vector_store.collection_name,
        )
        
        doc_store_path = Path(settings.vector_store.persist_directory).parent / "docstore"
        self.document_store = DocumentStore(persist_directory=str(doc_store_path))

        self.keyword_index = BM25Index(
            k1=settings.keyword_index.k1,
            b=settings.keyword_index.b,
        )

        # Try to load existing BM25 index
        self.keyword_index.load()

        self.retriever = HybridRetriever(
            vector_store=self.vector_store,
            keyword_index=self.keyword_index,
            document_store=self.document_store,
            vector_weight=settings.retrieval.vector_weight,
            keyword_weight=settings.retrieval.keyword_weight,
        )

        self.reranker = Reranker()

        self.context_builder = ContextBuilder(
            max_tokens=4000,
        )

        self.prompt_manager = PromptTemplateManager(
            templates_path=f"{settings.config_path}/prompts.yaml",
        )

        self.llm_service: Optional[LLMService] = None

        # Knowledge graph enhancer
        self.kg_enhancer = KnowledgeGraphEnhancer(
            config=settings.knowledge_graph,
            vector_store=self.vector_store,
            document_store=self.document_store,
        )
        self._load_kg_graph()

        # Cache manager
        self.cache_manager = CacheManager(
            config=settings.cache,
            embedding_service=self.embedding_service,
        )

    def _get_llm_service(self) -> LLMService:
        """Get or create LLM service"""
        if self.llm_service is None:
            api_key = self.settings.get_llm_api_key()
            self.llm_service = LLMService(
                provider=self.settings.llm.provider,
                api_key=api_key,
                model=self.settings.llm.model,
                base_url=self.settings.llm.base_url,
                max_tokens=self.settings.llm.max_tokens,
                temperature=self.settings.llm.temperature,
            )
        return self.llm_service

    def _load_kg_graph(self):
        """Load knowledge graph from file or build from chunks"""
        from pathlib import Path
        graph_path = Path(self.settings.knowledge_graph.graph_path)
        if graph_path.exists():
            self.kg_enhancer.load_graph()
        else:
            logger.info("[Pipeline] No graph.json found, KG will be built on first query if needed")

    async def aquery(self, question: str, top_k: int = 5) -> QAResponse:
        """Process a question and return answer asynchronously"""
        logger.info(f"[Pipeline] aquery: {question}")

        with tracer("rag_pipeline.aquery", question=question):
            # 1. Check L1 cache
            with tracer("cache_l1_lookup"):
                cached = self.cache_manager.get(question)
            if cached:
                logger.info("[Pipeline] L1 cache hit, returning cached response")
                return QAResponse(
                    answer=cached["answer"],
                    sources=cached.get("sources", []),
                    question_type=cached.get("question_type", ""),
                    keywords=cached.get("keywords", []),
                    metadata={**cached.get("metadata", {}), "cached": True, "cache_level": "L1"},
                )

            # 2. Embed the query
            with tracer("query_embedding"):
                t0 = time.time()
                query_embedding = self.cache_manager.get_embedding(question)
                if query_embedding:
                    logger.info("[Pipeline] L3 embedding cache hit")
                else:
                    import asyncio
                    loop = asyncio.get_running_loop()
                    query_embedding = await loop.run_in_executor(
                        None, self.embedding_service.embed_query, question
                    )
                    self.cache_manager.put_embedding(question, query_embedding)
                    logger.info(f"[Pipeline] Embedding done in {time.time()-t0:.2f}s")

            # 3. Check L2 semantic cache
            with tracer("cache_l2_lookup"):
                cached = self.cache_manager.get(question, query_embedding)
            if cached:
                logger.info("[Pipeline] L2 cache hit, returning cached response")
                return QAResponse(
                    answer=cached["answer"],
                    sources=cached.get("sources", []),
                    question_type=cached.get("question_type", ""),
                    keywords=cached.get("keywords", []),
                    metadata={**cached.get("metadata", {}), "cached": True, "cache_level": "L2"},
                )

            # 4. Retrieve relevant documents (async concurrency)
            with tracer("retrieval"):
                t0 = time.time()
                results = await self.retriever.aretrieve(
                    query=question,
                    query_embedding=query_embedding,
                    k=top_k * 2,
                )
                logger.info(f"[Pipeline] Retrieved {len(results)} results in {time.time()-t0:.2f}s")

            # 5. Rerank results
            if self.settings.retrieval.rerank:
                with tracer("rerank"):
                    results = self.reranker.rerank(results)

            # 6. Knowledge graph enhancement
            with tracer("kg_enhance"):
                results = self.kg_enhancer.enhance(results, question)
                results = results[:top_k]

            # 7. Classify question type
            with tracer("classify_question"):
                question_type = self._classify_question(question)

            # 8. Build context
            with tracer("build_context"):
                context = self.context_builder.build_context(results)

            # 9. Generate prompt
            with tracer("render_prompt"):
                prompt = self.prompt_manager.render(
                    question_type=question_type,
                    query=question,
                    context=context,
                )

            # 10. Generate answer
            with tracer("llm_generate", model=self.settings.llm.model):
                t0 = time.time()
                llm = self._get_llm_service()
                import asyncio
                loop = asyncio.get_running_loop()
                answer = await loop.run_in_executor(None, llm.generate, prompt)
                logger.info(f"[Pipeline] LLM generate done in {time.time()-t0:.2f}s")

            # 11. Get related topics
            with tracer("get_related_topics"):
                related_topics = self.kg_enhancer.get_related_topics(results)

            # 12. Build response and cache
            sources = self.context_builder.build_sources(results)
            response = QAResponse(
                answer=answer,
                sources=sources,
                question_type=question_type,
                keywords=self._extract_keywords(question),
                metadata={
                    "model": self.settings.llm.model,
                    "provider": self.settings.llm.provider,
                    "related_topics": related_topics,
                },
            )

            # Write to cache
            with tracer("cache_write"):
                self.cache_manager.put(question, query_embedding, {
                    "answer": answer,
                    "sources": sources,
                    "question_type": question_type,
                    "keywords": response.keywords,
                    "metadata": response.metadata,
                })

            return response

    def query(self, question: str, top_k: int = 5) -> QAResponse:
        """Process a question and return answer"""
        logger.info(f"[Pipeline] query: {question}")

        with tracer("rag_pipeline.query", question=question):
            # 1. Check L1 cache
            with tracer("cache_l1_lookup"):
                cached = self.cache_manager.get(question)
            if cached:
                logger.info("[Pipeline] L1 cache hit, returning cached response")
                return QAResponse(
                    answer=cached["answer"],
                    sources=cached.get("sources", []),
                    question_type=cached.get("question_type", ""),
                    keywords=cached.get("keywords", []),
                    metadata={**cached.get("metadata", {}), "cached": True, "cache_level": "L1"},
                )

            # 2. Embed the query (with L3 cache)
            with tracer("query_embedding"):
                t0 = time.time()
                query_embedding = self.cache_manager.get_embedding(question)
                if query_embedding:
                    logger.info("[Pipeline] L3 embedding cache hit")
                else:
                    query_embedding = self.embedding_service.embed_query(question)
                    self.cache_manager.put_embedding(question, query_embedding)
                    logger.info(f"[Pipeline] Embedding done in {time.time()-t0:.2f}s")

            # 3. Check L2 semantic cache
            with tracer("cache_l2_lookup"):
                cached = self.cache_manager.get(question, query_embedding)
            if cached:
                logger.info("[Pipeline] L2 cache hit, returning cached response")
                return QAResponse(
                    answer=cached["answer"],
                    sources=cached.get("sources", []),
                    question_type=cached.get("question_type", ""),
                    keywords=cached.get("keywords", []),
                    metadata={**cached.get("metadata", {}), "cached": True, "cache_level": "L2"},
                )

            # 4. Retrieve relevant documents
            with tracer("retrieval"):
                t0 = time.time()
                results = self.retriever.retrieve(
                    query=question,
                    query_embedding=query_embedding,
                    k=top_k * 2,
                )
                logger.info(f"[Pipeline] Retrieved {len(results)} results in {time.time()-t0:.2f}s")

            # 5. Rerank results
            if self.settings.retrieval.rerank:
                with tracer("rerank"):
                    results = self.reranker.rerank(results)

            # 6. Knowledge graph enhancement
            with tracer("kg_enhance"):
                results = self.kg_enhancer.enhance(results, question)
                results = results[:top_k]

            # 7. Classify question type
            with tracer("classify_question"):
                question_type = self._classify_question(question)

            # 8. Build context
            with tracer("build_context"):
                context = self.context_builder.build_context(results)

            # 9. Generate prompt
            with tracer("render_prompt"):
                prompt = self.prompt_manager.render(
                    question_type=question_type,
                    query=question,
                    context=context,
                )

            # 10. Generate answer
            with tracer("llm_generate", model=self.settings.llm.model):
                t0 = time.time()
                llm = self._get_llm_service()
                answer = llm.generate(prompt)
                logger.info(f"[Pipeline] LLM generate done in {time.time()-t0:.2f}s")

            # 11. Get related topics
            with tracer("get_related_topics"):
                related_topics = self.kg_enhancer.get_related_topics(results)

            # 12. Build response and cache
            sources = self.context_builder.build_sources(results)
            response = QAResponse(
                answer=answer,
                sources=sources,
                question_type=question_type,
                keywords=self._extract_keywords(question),
                metadata={
                    "model": self.settings.llm.model,
                    "provider": self.settings.llm.provider,
                    "related_topics": related_topics,
                },
            )

            # Write to cache
            with tracer("cache_write"):
                self.cache_manager.put(question, query_embedding, {
                    "answer": answer,
                    "sources": sources,
                    "question_type": question_type,
                    "keywords": response.keywords,
                    "metadata": response.metadata,
                })

            return response

    async def aquery_stream(
        self, question: str, top_k: int = 5
    ) -> tuple[dict, Any, dict]:
        """Process a question and return streaming answer asynchronously"""
        logger.info(f"[Pipeline] aquery_stream: {question}")

        with tracer("rag_pipeline.aquery_stream", question=question):
            with tracer("cache_l1_lookup"):
                cached = self.cache_manager.get(question)
            if cached:
                logger.info("[Pipeline] L1 cache hit, returning cached stream")
                metadata = {
                    "question_type": cached.get("question_type", ""),
                    "keywords": cached.get("keywords", []),
                    "sources": cached.get("sources", []),
                    "related_topics": cached.get("metadata", {}).get("related_topics", []),
                    "cached": True,
                    "cache_level": "L1",
                }
                return metadata, self._make_cached_stream(cached["answer"]), cached.get("metadata", {})

            with tracer("query_embedding"):
                t0 = time.time()
                query_embedding = self.cache_manager.get_embedding(question)
                if query_embedding:
                    logger.info("[Pipeline] L3 embedding cache hit")
                else:
                    import asyncio
                    loop = asyncio.get_running_loop()
                    query_embedding = await loop.run_in_executor(
                        None, self.embedding_service.embed_query, question
                    )
                    self.cache_manager.put_embedding(question, query_embedding)
                    logger.info(f"[Pipeline] Embedding done in {time.time()-t0:.2f}s")

            with tracer("cache_l2_lookup"):
                cached = self.cache_manager.get(question, query_embedding)
            if cached:
                logger.info("[Pipeline] L2 cache hit, returning cached stream")
                metadata = {
                    "question_type": cached.get("question_type", ""),
                    "keywords": cached.get("keywords", []),
                    "sources": cached.get("sources", []),
                    "related_topics": cached.get("metadata", {}).get("related_topics", []),
                    "cached": True,
                    "cache_level": "L2",
                }
                return metadata, self._make_cached_stream(cached["answer"]), cached.get("metadata", {})

            with tracer("retrieval"):
                t0 = time.time()
                results = await self.retriever.aretrieve(
                    query=question,
                    query_embedding=query_embedding,
                    k=top_k * 2,
                )
                logger.info(f"[Pipeline] Retrieved {len(results)} results in {time.time()-t0:.2f}s")

            if self.settings.retrieval.rerank:
                with tracer("rerank"):
                    results = self.reranker.rerank(results)

            with tracer("kg_enhance"):
                results = self.kg_enhancer.enhance(results, question)
                results = results[:top_k]

            with tracer("classify_question"):
                question_type = self._classify_question(question)

            with tracer("build_context"):
                context = self.context_builder.build_context(results)

            with tracer("render_prompt"):
                prompt = self.prompt_manager.render(
                    question_type=question_type,
                    query=question,
                    context=context,
                )

            with tracer("build_metadata"):
                related_topics = self.kg_enhancer.get_related_topics(results)
                sources = self.context_builder.build_sources(results)
                metadata = {
                    "question_type": question_type,
                    "keywords": self._extract_keywords(question),
                    "sources": sources,
                    "related_topics": related_topics,
                }

            with tracer("llm_generate_stream", model=self.settings.llm.model):
                logger.info("[Pipeline] Starting LLM stream generation...")
                llm = self._get_llm_service()
                
                import asyncio
                loop = asyncio.get_running_loop()
                stream = await loop.run_in_executor(None, llm.generate_stream, prompt)

                async def caching_stream():
                    full_answer = ""
                    for chunk in stream:
                        full_answer += chunk
                        yield chunk
                    self.cache_manager.put(question, query_embedding, {
                        "answer": full_answer,
                        "sources": sources,
                        "question_type": question_type,
                        "keywords": metadata["keywords"],
                        "metadata": {"model": self.settings.llm.model, "related_topics": related_topics},
                    })

                return metadata, caching_stream(), {"model": self.settings.llm.model}
        """Process a question and return streaming answer"""
        logger.info(f"[Pipeline] query_stream: {question}")

        with tracer("rag_pipeline.query_stream", question=question):
            # 1. Check L1 cache
            with tracer("cache_l1_lookup"):
                cached = self.cache_manager.get(question)
            if cached:
                logger.info("[Pipeline] L1 cache hit, returning cached stream")
                metadata = {
                    "question_type": cached.get("question_type", ""),
                    "keywords": cached.get("keywords", []),
                    "sources": cached.get("sources", []),
                    "related_topics": cached.get("metadata", {}).get("related_topics", []),
                    "cached": True,
                    "cache_level": "L1",
                }
                return metadata, self._make_cached_stream(cached["answer"]), cached.get("metadata", {})

            # 2. Embed the query (with L3 cache)
            with tracer("query_embedding"):
                t0 = time.time()
                query_embedding = self.cache_manager.get_embedding(question)
                if query_embedding:
                    logger.info("[Pipeline] L3 embedding cache hit")
                else:
                    query_embedding = self.embedding_service.embed_query(question)
                    self.cache_manager.put_embedding(question, query_embedding)
                    logger.info(f"[Pipeline] Embedding done in {time.time()-t0:.2f}s")

            # 3. Check L2 semantic cache
            with tracer("cache_l2_lookup"):
                cached = self.cache_manager.get(question, query_embedding)
            if cached:
                logger.info("[Pipeline] L2 cache hit, returning cached stream")
                metadata = {
                    "question_type": cached.get("question_type", ""),
                    "keywords": cached.get("keywords", []),
                    "sources": cached.get("sources", []),
                    "related_topics": cached.get("metadata", {}).get("related_topics", []),
                    "cached": True,
                    "cache_level": "L2",
                }
                return metadata, self._make_cached_stream(cached["answer"]), cached.get("metadata", {})

            # 4. Retrieve relevant documents
            with tracer("retrieval"):
                t0 = time.time()
                results = self.retriever.retrieve(
                    query=question,
                    query_embedding=query_embedding,
                    k=top_k * 2,
                )
                logger.info(f"[Pipeline] Retrieved {len(results)} results in {time.time()-t0:.2f}s")

            # 5. Rerank results
            if self.settings.retrieval.rerank:
                with tracer("rerank"):
                    results = self.reranker.rerank(results)

            # 6. Knowledge graph enhancement
            with tracer("kg_enhance"):
                results = self.kg_enhancer.enhance(results, question)
                results = results[:top_k]

            # 7. Classify question type
            with tracer("classify_question"):
                question_type = self._classify_question(question)

            # 8. Build context
            with tracer("build_context"):
                context = self.context_builder.build_context(results)

            # 9. Generate prompt
            with tracer("render_prompt"):
                prompt = self.prompt_manager.render(
                    question_type=question_type,
                    query=question,
                    context=context,
                )

            # 10. Build metadata
            with tracer("build_metadata"):
                related_topics = self.kg_enhancer.get_related_topics(results)
                sources = self.context_builder.build_sources(results)
                metadata = {
                    "question_type": question_type,
                    "keywords": self._extract_keywords(question),
                    "sources": sources,
                    "related_topics": related_topics,
                }

            # 11. Generate streaming answer with cache collection
            with tracer("llm_generate_stream", model=self.settings.llm.model):
                logger.info("[Pipeline] Starting LLM stream generation...")
                llm = self._get_llm_service()
                stream = llm.generate_stream(prompt)

                # Wrap stream to collect full answer for caching
                def caching_stream():
                    full_answer = ""
                    for chunk in stream:
                        full_answer += chunk
                        yield chunk
                    # Write to cache after stream completes
                    self.cache_manager.put(question, query_embedding, {
                        "answer": full_answer,
                        "sources": sources,
                        "question_type": question_type,
                        "keywords": metadata["keywords"],
                        "metadata": {"model": self.settings.llm.model, "related_topics": related_topics},
                    })

                return metadata, caching_stream(), {"model": self.settings.llm.model}

    def _make_cached_stream(self, answer: str) -> Iterator[str]:
        """Convert cached full answer to a simulated stream"""
        # Split by sentences for natural streaming feel
        import re
        sentences = re.split(r"(?<=[。！？\n])", answer)
        for sentence in sentences:
            if sentence.strip():
                yield sentence

    def _classify_question(self, question: str) -> str:
        """Classify question type"""
        question_lower = question.lower()

        if any(kw in question_lower for kw in ["怎么定位", "如何定位", "定位方法", "定位流程"]):
            return "定位指导"
        elif any(kw in question_lower for kw in ["是什么原因", "为什么", "怎么办", "如何解决"]):
            return "问题诊断"
        elif any(kw in question_lower for kw in ["怎么用", "如何使用", "命令", "参数"]):
            return "工具使用"
        elif any(kw in question_lower for kw in ["什么是", "概念", "含义", "定义"]):
            return "概念理解"
        elif any(kw in question_lower for kw in ["如何查看", "怎么操作", "步骤", "界面"]):
            return "操作步骤"
        else:
            return "默认"

    def _extract_keywords(self, question: str) -> List[str]:
        """Extract keywords from question"""
        import jieba

        # Keywords to look for
        keyword_patterns = [
            "msprof", "MindStudio", "性能分析", "性能优化", "通信",
            "算子", "快慢卡", "Host Bound", "下发", "AI Core",
            "AI CPU", "Cube", "MTE", "通算并行", "通信重传",
        ]

        keywords = []
        for kw in keyword_patterns:
            if kw.lower() in question.lower():
                keywords.append(kw)

        # Also extract nouns using jieba
        words = jieba.lcut(question)
        keywords.extend([w for w in words if len(w) > 1 and w not in keywords])

        return list(set(keywords))[:10]