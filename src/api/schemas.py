"""API schemas"""

from typing import List, Optional

from pydantic import BaseModel, Field


class QARequest(BaseModel):
    """QA request schema"""

    query: str = Field(..., min_length=1, max_length=1000, description="用户问题")
    options: Optional[dict] = Field(
        default_factory=lambda: {"top_k": 5, "include_sources": True},
        description="可选参数",
    )


class SourceDocument(BaseModel):
    """Source document schema"""

    doc_id: str
    title: str
    section: str
    source_url: str
    relevance_score: float


class QAResponse(BaseModel):
    """QA response schema"""

    code: int = 0
    message: str = "success"
    data: dict


class RetrieveRequest(BaseModel):
    """Retrieve request schema"""

    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=10, ge=1, le=50)
    retrieval_type: str = Field(default="hybrid")


class RetrieveResult(BaseModel):
    """Retrieve result schema"""

    chunk_id: str
    doc_id: str
    doc_title: str
    section_title: str
    content: str
    source_url: str
    score: float


class RetrieveResponse(BaseModel):
    """Retrieve response schema"""

    code: int = 0
    data: dict


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    version: str
    vector_store_count: int
    keyword_index_count: int


class CacheClearRequest(BaseModel):
    """Cache clear request"""

    level: Optional[str] = Field(
        default="all",
        description="Cache level to clear: 'all', 'l1', 'l2', 'l3'",
    )