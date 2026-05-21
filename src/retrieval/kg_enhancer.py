"""Knowledge Graph Enhancer for retrieval results"""

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from ..core.config import KnowledgeGraphConfig
from .hybrid_retriever import HybridResult

logger = logging.getLogger("ms_rag")


@dataclass
class RelatedTopic:
    """Related topic for recommendation"""

    title: str
    doc_id: str
    relation: str  # "parent" | "child" | "sibling" | "reference"

    def to_dict(self) -> dict:
        return {"title": self.title, "doc_id": self.doc_id, "relation": self.relation}


class DocumentGraph:
    """Document relationship graph built from metadata"""

    def __init__(self):
        self.parent_map: Dict[str, str] = {}
        self.children_map: Dict[str, List[str]] = {}
        self.doc_chunks_map: Dict[str, List[str]] = {}
        self.doc_titles: Dict[str, str] = {}
        self.references: Dict[str, List[str]] = {}

    @classmethod
    def from_json(cls, path: str) -> "DocumentGraph":
        graph = cls()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        graph.parent_map = data.get("parent_map", {})
        graph.children_map = data.get("children_map", {})
        graph.doc_chunks_map = data.get("doc_chunks_map", {})
        graph.doc_titles = data.get("doc_titles", {})
        graph.references = data.get("references", {})
        return graph

    @classmethod
    def from_chunks(cls, chunks: list) -> "DocumentGraph":
        """Build graph from chunk metadata (fallback when no graph.json)"""
        graph = cls()

        # Collect doc info from chunk metadata
        for chunk in chunks:
            meta = chunk.metadata if hasattr(chunk, "metadata") else chunk.get("metadata", {})
            doc_id = meta.get("doc_id", "")
            if not doc_id:
                continue

            # doc title
            doc_title = meta.get("doc_title", "")
            if doc_title and doc_id not in graph.doc_titles:
                graph.doc_titles[doc_id] = doc_title

            # parent relationship
            parent_topic = meta.get("parent_topic", "")
            if parent_topic:
                graph.parent_map[doc_id] = parent_topic
                graph.children_map.setdefault(parent_topic, [])
                if doc_id not in graph.children_map[parent_topic]:
                    graph.children_map[parent_topic].append(doc_id)

            # chunk mapping
            chunk_id = chunk.chunk_id if hasattr(chunk, "chunk_id") else chunk.get("chunk_id", "")
            graph.doc_chunks_map.setdefault(doc_id, [])
            if chunk_id not in graph.doc_chunks_map[doc_id]:
                graph.doc_chunks_map[doc_id].append(chunk_id)

        return graph

    def get_parent(self, doc_id: str) -> Optional[str]:
        return self.parent_map.get(doc_id)

    def get_children(self, doc_id: str) -> List[str]:
        return self.children_map.get(doc_id, [])

    def get_siblings(self, doc_id: str) -> List[str]:
        parent = self.parent_map.get(doc_id)
        if not parent:
            return []
        siblings = self.children_map.get(parent, [])
        return [s for s in siblings if s != doc_id]

    def get_references(self, doc_id: str) -> List[str]:
        return self.references.get(doc_id, [])

    def get_first_chunk(self, doc_id: str) -> Optional[str]:
        chunks = self.doc_chunks_map.get(doc_id, [])
        return chunks[0] if chunks else None


class KnowledgeGraphEnhancer:
    """Enhance retrieval results using document graph relationships"""

    def __init__(
        self,
        config: KnowledgeGraphConfig,
        vector_store=None,
        document_store=None,
    ):
        self.config = config
        self.vector_store = vector_store
        self.document_store = document_store
        self.graph: Optional[DocumentGraph] = None

    def load_graph(self, chunks: list = None):
        """Load or build the document graph"""
        graph_path = Path(self.config.graph_path)
        if graph_path.exists():
            self.graph = DocumentGraph.from_json(str(graph_path))
            logger.info(
                f"[KG] Loaded graph: {len(self.graph.doc_titles)} docs, "
                f"{len(self.graph.parent_map)} parent links"
            )
        elif chunks:
            self.graph = DocumentGraph.from_chunks(chunks)
            logger.info(
                f"[KG] Built graph from chunks: {len(self.graph.doc_titles)} docs, "
                f"{len(self.graph.parent_map)} parent links"
            )
        else:
            logger.warning("[KG] No graph available, enhancement disabled")
            self.graph = None

    def enhance(self, results: List[HybridResult], query: str) -> List[HybridResult]:
        """Enhance results with related documents from the graph"""
        if not self.config.enabled or not self.graph:
            return results

        original_doc_ids = {r.doc_id for r in results}
        expanded: List[HybridResult] = []

        # Find the highest score among original results for weighting
        max_score = max((r.final_score for r in results), default=0.0)

        # Collect expansion candidates
        seen_doc_ids = set(original_doc_ids)
        for result in results:
            doc_id = result.doc_id

            # Upward: parent document
            if self.config.expand_parent:
                parent_id = self.graph.get_parent(doc_id)
                if parent_id and parent_id not in seen_doc_ids:
                    expanded.append(self._make_expanded_result(
                        parent_id, "parent", result, max_score,
                        self.config.expand_weight_parent,
                    ))
                    seen_doc_ids.add(parent_id)

            # Sideways: sibling documents
            if self.config.expand_sibling:
                siblings = self.graph.get_siblings(doc_id)
                for sid in siblings[:self.config.max_expand_per_direction]:
                    if sid not in seen_doc_ids:
                        expanded.append(self._make_expanded_result(
                            sid, "sibling", result, max_score,
                            self.config.expand_weight_sibling,
                        ))
                        seen_doc_ids.add(sid)

            # Downward: child documents
            if self.config.expand_child:
                children = self.graph.get_children(doc_id)
                for cid in children[:self.config.max_expand_per_direction]:
                    if cid not in seen_doc_ids:
                        expanded.append(self._make_expanded_result(
                            cid, "child", result, max_score,
                            self.config.expand_weight_child,
                        ))
                        seen_doc_ids.add(cid)

            # References
            if self.config.expand_reference:
                refs = self.graph.get_references(doc_id)
                for rid in refs[:self.config.max_expand_per_direction]:
                    if rid not in seen_doc_ids:
                        expanded.append(self._make_expanded_result(
                            rid, "reference", result, max_score,
                            self.config.expand_weight_reference,
                        ))
                        seen_doc_ids.add(rid)

        # Sort expanded by final_score desc, keep top N
        expanded.sort(key=lambda x: x.final_score, reverse=True)
        expanded = expanded[:self.config.max_enhanced_results]

        # Merge: keep original order, insert expanded at end
        enhanced = results + expanded
        logger.info(
            f"[KG] Original: {len(results)}, Expanded: {len(expanded)}, "
            f"Total: {len(enhanced)}"
        )
        return enhanced

    def get_related_topics(self, results: List[HybridResult]) -> List[dict]:
        """Get related topics for recommendation"""
        if not self.config.enabled or not self.graph:
            return []

        result_doc_ids = {r.doc_id for r in results}
        topics: List[RelatedTopic] = []
        seen = set()

        for result in results:
            doc_id = result.doc_id

            # Parent
            parent_id = self.graph.get_parent(doc_id)
            if parent_id and parent_id not in result_doc_ids and parent_id not in seen:
                title = self.graph.doc_titles.get(parent_id, parent_id)
                topics.append(RelatedTopic(title=title, doc_id=parent_id, relation="parent"))
                seen.add(parent_id)

            # Children
            for cid in self.graph.get_children(doc_id):
                if cid not in result_doc_ids and cid not in seen:
                    title = self.graph.doc_titles.get(cid, cid)
                    topics.append(RelatedTopic(title=title, doc_id=cid, relation="child"))
                    seen.add(cid)

            # Siblings
            for sid in self.graph.get_siblings(doc_id):
                if sid not in result_doc_ids and sid not in seen:
                    title = self.graph.doc_titles.get(sid, sid)
                    topics.append(RelatedTopic(title=title, doc_id=sid, relation="sibling"))
                    seen.add(sid)

        # Sort by relation priority: parent > child > sibling > reference
        priority = {"parent": 0, "child": 1, "sibling": 2, "reference": 3}
        topics.sort(key=lambda t: priority.get(t.relation, 9))

        return [t.to_dict() for t in topics[:self.config.related_topics_count]]

    def _make_expanded_result(
        self,
        doc_id: str,
        relation: str,
        source_result: HybridResult,
        max_score: float,
        weight: float,
    ) -> HybridResult:
        """Create a HybridResult for an expanded document"""
        chunk_id = self.graph.get_first_chunk(doc_id)
        content = ""
        section_title = ""
        source_url = ""
        images = []

        if chunk_id and self.document_store:
            try:
                doc_data = self.document_store.get_document(chunk_id)
                if doc_data:
                    content = doc_data.get("content", "")
                    section_title = doc_data.get("section_title", "")
                    source_url = doc_data.get("source_url", "")
                    images = doc_data.get("images", [])
            except Exception:
                pass
                
        if not content and chunk_id and self.vector_store:
            try:
                chunk_data = self.vector_store.get_chunk(chunk_id)
                if chunk_data:
                    content = chunk_data.get("content", "")
                    section_title = chunk_data.get("section_title", "")
                    source_url = chunk_data.get("source_url", "")
                    images = chunk_data.get("images", [])
            except Exception:
                pass

        doc_title = self.graph.doc_titles.get(doc_id, doc_id)

        return HybridResult(
            chunk_id=chunk_id or f"{doc_id}_expanded",
            doc_id=doc_id,
            doc_title=doc_title,
            section_title=section_title or f"[{relation}] {doc_title}",
            content=content,
            source_url=source_url,
            vector_score=0.0,
            keyword_score=0.0,
            final_score=max_score * weight,
            images=images,
        )
