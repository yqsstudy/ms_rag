"""Main application entry point"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.routes import router
from .core.config import get_settings
from .core.logging import setup_logging
from .core.tracing import TraceContext, trace_context_var


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    settings = get_settings()
    setup_logging(
        level=settings.logging.level,
        log_format=settings.logging.format,
        log_file=settings.logging.file,
    )

    logger = logging.getLogger("ms_rag")
    logger.info(f"Starting MS-RAG API server...")
    logger.info(f"LLM Provider: {settings.llm.provider}")
    logger.info(f"Embedding Model: {settings.embedding.model}")

    yield

    # Shutdown
    logger.info("Shutting down MS-RAG API server...")


def create_app() -> FastAPI:
    """Create FastAPI application"""
    settings = get_settings()

    app = FastAPI(
        title="MS-RAG API",
        description="性能定位指南RAG系统 - 昇腾AI计算平台智能问答系统",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def trace_middleware(request: Request, call_next):
        trace_ctx = TraceContext()
        token = trace_context_var.set(trace_ctx)
        try:
            response = await call_next(request)
            trace_ctx.finish(path=request.url.path, method=request.method, status_code=response.status_code)
            return response
        except Exception as e:
            trace_ctx.finish(path=request.url.path, method=request.method, error=str(e))
            raise
        finally:
            trace_context_var.reset(token)

    # Include routers
    app.include_router(router, prefix="/api/v1")

    # Mount corpus directory for images
    corpus_path = Path("./corpus")
    if corpus_path.exists():
        app.mount("/corpus", StaticFiles(directory="corpus"), name="corpus")

    # Mount static files for frontend (if exists)
    static_path = Path("./static")
    if static_path.exists():
        app.mount("/", StaticFiles(directory="static", html=True), name="static")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.debug,
    )