"""RAG Pipeline"""

from dataclasses import dataclass
from typing import Iterator, List, Optional

from ..core.config import Settings
from ..embeddings.embedding import EmbeddingService
from ..generation.context_builder import ContextBuilder
from ..generation.llm_service import LLMService
from ..generation.prompt_templates import PromptTemplateManager
from ..retrieval.hybrid_retriever import HybridRetriever, HybridResult
from ..retrieval.reranker import Reranker
from ..storage.keyword_index import BM25Index
from ..storage.vector_store import VectorStore


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

        self.keyword_index = BM25Index(
            k1=settings.keyword_index.k1,
            b=settings.keyword_index.b,
        )

        # Try to load existing BM25 index
        self.keyword_index.load()

        self.retriever = HybridRetriever(
            vector_store=self.vector_store,
            keyword_index=self.keyword_index,
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

    def _get_llm_service(self) -> LLMService:
        """Get or create LLM service"""
        if self.llm_service is None:
            api_key = self.settings.get_llm_api_key()
            self.llm_service = LLMService(
                provider=self.settings.llm.provider,
                api_key=api_key,
                model=self.settings.llm.model,
                max_tokens=self.settings.llm.max_tokens,
                temperature=self.settings.llm.temperature,
            )
        return self.llm_service

    def query(self, question: str, top_k: int = 5) -> QAResponse:
        """Process a question and return answer"""
        # 1. Embed the query
        query_embedding = self.embedding_service.embed_query(question)

        # 2. Retrieve relevant documents
        results = self.retriever.retrieve(
            query=question,
            query_embedding=query_embedding,
            k=top_k * 2,
        )

        # 3. Rerank results
        if self.settings.retrieval.rerank:
            results = self.reranker.rerank(results)

        results = results[:top_k]

        # 4. Classify question type
        question_type = self._classify_question(question)

        # 5. Build context
        context = self.context_builder.build_context(results)

        # 6. Generate prompt
        prompt = self.prompt_manager.render(
            question_type=question_type,
            query=question,
            context=context,
        )

        # 7. Generate answer
        llm = self._get_llm_service()
        answer = llm.generate(prompt)

        # 8. Build response
        return QAResponse(
            answer=answer,
            sources=self.context_builder.build_sources(results),
            question_type=question_type,
            keywords=self._extract_keywords(question),
            metadata={
                "model": self.settings.llm.model,
                "provider": self.settings.llm.provider,
            },
        )

    def query_stream(
        self, question: str, top_k: int = 5
    ) -> tuple[dict, Iterator[str], dict]:
        """Process a question and return streaming answer"""
        # 1. Embed the query
        query_embedding = self.embedding_service.embed_query(question)

        # 2. Retrieve relevant documents
        results = self.retriever.retrieve(
            query=question,
            query_embedding=query_embedding,
            k=top_k * 2,
        )

        # 3. Rerank results
        if self.settings.retrieval.rerank:
            results = self.reranker.rerank(results)

        results = results[:top_k]

        # 4. Classify question type
        question_type = self._classify_question(question)

        # 5. Build context
        context = self.context_builder.build_context(results)

        # 6. Generate prompt
        prompt = self.prompt_manager.render(
            question_type=question_type,
            query=question,
            context=context,
        )

        # 7. Build metadata
        metadata = {
            "question_type": question_type,
            "keywords": self._extract_keywords(question),
            "sources": self.context_builder.build_sources(results),
        }

        # 8. Generate streaming answer
        llm = self._get_llm_service()
        stream = llm.generate_stream(prompt)

        return metadata, stream, {"model": self.settings.llm.model}

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