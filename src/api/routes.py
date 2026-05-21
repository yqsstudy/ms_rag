"""API routes"""

import json
import logging
import time
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..core.config import get_settings
from ..pipeline.rag_pipeline import RAGPipeline
from .schemas import (
    CacheClearRequest,
    HealthResponse,
    QARequest,
    QAResponse,
    RetrieveRequest,
    RetrieveResponse,
)

logger = logging.getLogger("ms_rag")

router = APIRouter()

# Global pipeline instance
_pipeline: RAGPipeline = None


def get_pipeline() -> RAGPipeline:
    """Get or create pipeline instance"""
    global _pipeline
    if _pipeline is None:
        settings = get_settings()
        _pipeline = RAGPipeline(settings)
    return _pipeline


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    pipeline = get_pipeline()
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        vector_store_count=pipeline.vector_store.count(),
        keyword_index_count=pipeline.keyword_index.count(),
    )


@router.post("/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    """Question answering endpoint"""
    start_time = time.time()
    logger.info(f"[QA] Received query: {request.query}")

    try:
        pipeline = get_pipeline()
        top_k = request.options.get("top_k", 5)

        response = await pipeline.aquery(request.query, top_k=top_k)

        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(f"[QA] Completed in {response_time_ms}ms, type={response.question_type}")

        return QAResponse(
            code=0,
            message="success",
            data={
                "answer": response.answer,
                "question_type": response.question_type,
                "keywords": response.keywords,
                "sources": response.sources,
                "metadata": {
                    **response.metadata,
                    "response_time_ms": response_time_ms,
                },
            },
        )

    except Exception as e:
        logger.error(f"[QA] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/qa/stream")
async def qa_stream_endpoint(request: QARequest):
    """Streaming question answering endpoint"""

    async def generate() -> AsyncIterator[str]:
        start_time = time.time()
        logger.info(f"[Stream] Received query: {request.query}")

        try:
            pipeline = get_pipeline()
            top_k = request.options.get("top_k", 5)

            # Get streaming response
            logger.info("[Stream] Starting pipeline.aquery_stream...")
            metadata, stream_gen, model_info = await pipeline.aquery_stream(
                request.query, top_k=top_k
            )
            logger.info(f"[Stream] Pipeline returned, model={model_info}")

            # Send metadata event
            metadata_json = json.dumps(metadata, ensure_ascii=False)
            logger.info(f"[Stream] Sending metadata: {metadata_json[:200]}")
            yield f"event: metadata\ndata: {metadata_json}\n\n"

            # Stream answer chunks
            chunk_count = 0
            if hasattr(stream_gen, "__aiter__"):
                async for chunk in stream_gen:
                    if chunk:
                        yield f"event: answer\ndata: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
                        chunk_count += 1
            else:
                for chunk in stream_gen:
                    if chunk:
                        yield f"event: answer\ndata: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
                        chunk_count += 1
                        # simulate async yield for sync generators
                        import asyncio
                        await asyncio.sleep(0)

            logger.info(f"[Stream] Stream finished, sent {chunk_count} chunks")

            # Send done event
            response_time_ms = int((time.time() - start_time) * 1000)
            done_data = {
                "tokens_used": 0,
                "response_time_ms": response_time_ms,
                "model": model_info.get("model"),
            }
            yield f"event: done\ndata: {json.dumps(done_data, ensure_ascii=False)}\n\n"
            logger.info(f"[Stream] Completed in {response_time_ms}ms")

        except Exception as e:
            logger.error(f"[Stream] Error: {e}", exc_info=True)
            error_data = {"error": str(e)}
            yield f"event: error\ndata: {json.dumps(error_data, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_endpoint(request: RetrieveRequest):
    """Document retrieval endpoint"""
    try:
        pipeline = get_pipeline()

        import asyncio
        loop = asyncio.get_running_loop()
        query_embedding = await loop.run_in_executor(
            None, pipeline.embedding_service.embed_query, request.query
        )

        # Retrieve documents
        results = await pipeline.retriever.aretrieve(
            query=request.query,
            query_embedding=query_embedding,
            k=request.top_k,
        )

        # Rerank if enabled
        if pipeline.settings.retrieval.rerank:
            results = pipeline.reranker.rerank(results)

        return RetrieveResponse(
            code=0,
            data={
                "results": [r.to_dict() for r in results[: request.top_k]],
                "total": len(results),
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/clear")
async def cache_clear_endpoint(request: CacheClearRequest):
    """Clear cache entries"""
    try:
        pipeline = get_pipeline()
        level = request.level or "all"
        pipeline.cache_manager.clear(level=level)
        logger.info(f"[Cache] Cleared cache level={level}")
        return {"code": 0, "message": f"Cache cleared: {level}"}
    except Exception as e:
        logger.error(f"[Cache] Clear error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats")
async def cache_stats_endpoint():
    """Get cache statistics"""
    try:
        pipeline = get_pipeline()
        stats = pipeline.cache_manager.get_stats()
        return {"code": 0, "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))