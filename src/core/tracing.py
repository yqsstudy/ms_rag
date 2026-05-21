"""Tracing and Observability utilities"""

import contextvars
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .logging import get_logger

logger = get_logger("ms_rag.tracing")

# Global context var to hold the current trace context
trace_context_var: contextvars.ContextVar[Optional["TraceContext"]] = contextvars.ContextVar(
    "trace_context", default=None
)

def get_trace_id() -> str:
    """Get current trace ID or return empty string"""
    ctx = trace_context_var.get()
    return ctx.trace_id if ctx else ""

@dataclass
class Span:
    """A single operation within a trace"""
    name: str
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def finish(self, **kwargs):
        """Mark span as finished and add optional metadata"""
        self.end_time = time.time()
        self.metadata.update(kwargs)
        
    @property
    def duration_ms(self) -> float:
        if not self.end_time:
            return 0.0
        return (self.end_time - self.start_time) * 1000

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "span_id": self.span_id,
            "duration_ms": round(self.duration_ms, 2),
            "metadata": self.metadata,
        }

class TraceContext:
    """Holds all spans and metadata for a single request lifecycle"""
    
    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.start_time = time.time()
        self.spans: List[Span] = []
        self.metadata: Dict[str, Any] = {}
        
    def add_span(self, span: Span):
        self.spans.append(span)

    def finish(self, **kwargs):
        self.metadata.update(kwargs)
        duration = (time.time() - self.start_time) * 1000
        
        # Log the full trace summary
        trace_data = {
            "trace_id": self.trace_id,
            "total_duration_ms": round(duration, 2),
            "spans": [s.to_dict() for s in self.spans],
            "metadata": self.metadata
        }
        
        logger.info(f"[TRACE_SUMMARY] {json.dumps(trace_data, ensure_ascii=False)}")

class tracer:
    """Context manager for creating a span"""
    
    def __init__(self, name: str, **metadata):
        self.name = name
        self.metadata = metadata
        self.span: Optional[Span] = None
        self.ctx: Optional[TraceContext] = None

    def __enter__(self):
        self.ctx = trace_context_var.get()
        if self.ctx:
            self.span = Span(name=self.name, metadata=self.metadata)
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span and self.ctx:
            if exc_type:
                self.span.metadata["error"] = str(exc_val)
            self.span.finish()
            self.ctx.add_span(self.span)
