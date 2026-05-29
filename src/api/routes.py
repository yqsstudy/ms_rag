"""API routes"""

import asyncio
import json
import logging
import time
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse

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
_ALLOWED_CACHE_LEVELS = {"all", "l1", "l2", "l3"}


def get_pipeline(request: Request) -> RAGPipeline:
    pipeline = getattr(request.app.state, "pipeline", None)
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG pipeline is not ready",
        )
    return pipeline


def require_admin(request: Request) -> None:
    admin_token = getattr(request.app.state.settings.api, "admin_token", None)
    if not admin_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin API is disabled",
        )
    if request.headers.get("x-admin-token") != admin_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin token",
        )


def internal_error(endpoint: str, exc: Exception) -> HTTPException:
    logger.error("[%s] Internal error: %s", endpoint, exc, exc_info=True)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error",
    )


@router.get("/health", response_model=HealthResponse)
async def health_check(pipeline: RAGPipeline = Depends(get_pipeline)):
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        vector_store_count=pipeline.vector_store.count(),
        keyword_index_count=pipeline.keyword_index.count(),
    )


@router.post("/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest, pipeline: RAGPipeline = Depends(get_pipeline)):
    """Question answering endpoint"""
    start_time = time.time()
    logger.info("[QA] Received query length=%s", len(request.query))

    try:
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

    except HTTPException:
        raise
    except Exception as e:
        raise internal_error("QA", e)


@router.post("/qa/stream")
async def qa_stream_endpoint(request: QARequest, pipeline: RAGPipeline = Depends(get_pipeline)):
    """Streaming question answering endpoint"""

    async def generate() -> AsyncIterator[str]:
        start_time = time.time()
        logger.info("[Stream] Received query length=%s", len(request.query))

        try:
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
                        await asyncio.sleep(0)

            logger.info(f"[Stream] Stream finished, sent {chunk_count} chunks")

            # Send done event
            response_time_ms = int((time.time() - start_time) * 1000)
            done_data = {
                "response_time_ms": response_time_ms,
                "model": model_info.get("model"),
            }
            yield f"event: done\ndata: {json.dumps(done_data, ensure_ascii=False)}\n\n"
            logger.info(f"[Stream] Completed in {response_time_ms}ms")

        except Exception as e:
            logger.error("[Stream] Error: %s", e, exc_info=True)
            error_data = {"error": "Internal server error"}
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
async def retrieve_endpoint(request: RetrieveRequest, pipeline: RAGPipeline = Depends(get_pipeline)):
    """Document retrieval endpoint"""
    try:
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
            results = pipeline.reranker.rerank(results, request.query)

        return RetrieveResponse(
            code=0,
            data={
                "results": [r.to_dict() for r in results[: request.top_k]],
                "total": len(results),
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise internal_error("Retrieve", e)


@router.post("/cache/clear", dependencies=[Depends(require_admin)])
async def cache_clear_endpoint(
    request: CacheClearRequest,
    pipeline: RAGPipeline = Depends(get_pipeline),
):
    """Clear cache entries"""
    try:
        level = request.level or "all"
        if level not in _ALLOWED_CACHE_LEVELS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid cache level",
            )
        pipeline.cache_manager.clear(level=level)
        logger.info("[Cache] Cleared cache level=%s", level)
        return {"code": 0, "message": f"Cache cleared: {level}"}
    except HTTPException:
        raise
    except Exception as e:
        raise internal_error("Cache", e)


@router.get("/cache/stats", dependencies=[Depends(require_admin)])
async def cache_stats_endpoint(pipeline: RAGPipeline = Depends(get_pipeline)):
    """Get cache statistics"""
    try:
        stats = pipeline.cache_manager.get_stats()
        return {"code": 0, "data": stats}
    except HTTPException:
        raise
    except Exception as e:
        raise internal_error("Cache", e)
