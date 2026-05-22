"""Metadata extractor for documents"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentMetadata:
    """Document metadata"""

    doc_id: str
    title: str
    source_url: str
    parent_topic: Optional[str] = None
    child_topics: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    links: list[dict] = field(default_factory=list)


class MetadataExtractor:
    """Extract metadata from documents"""

    # Keywords related to performance optimization
    KEYWORD_PATTERNS = [
        r"msprof",
        r"MindStudio",
        r"性能分析",
        r"性能优化",
        r"通信",
        r"算子",
        r"快慢卡",
        r"Host Bound",
        r"下发",
        r"AI Core",
        r"AI CPU",
        r"Cube",
        r"MTE",
        r"通算并行",
        r"通信重传",
        r"融合算子",
        r"性能采集",
        r"性能调优",
    ]

    def __init__(self):
        self.keyword_pattern = re.compile(
            "|".join(self.KEYWORD_PATTERNS), re.IGNORECASE
        )
        self.link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        self.image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
        self.parent_topic_pattern = re.compile(r"父主题[：:]\s*(\S+)")

    def extract(self, doc: "Document", content: str = None) -> DocumentMetadata:
        """Extract metadata from document"""
        if content is None:
            content = doc.content

        return DocumentMetadata(
            doc_id=doc.doc_id,
            title=doc.title,
            source_url=doc.source_url,
            parent_topic=self._extract_parent_topic(content),
            keywords=self._extract_keywords(content),
            images=self._extract_images(content),
            links=self._extract_links(content),
        )

    def _extract_parent_topic(self, content: str) -> Optional[str]:
        """Extract parent topic from content"""
        match = self.parent_topic_pattern.search(content)
        return match.group(1) if match else None

    def _extract_keywords(self, content: str) -> list[str]:
        """Extract keywords from content"""
        matches = self.keyword_pattern.findall(content)
        # Remove duplicates while preserving order
        seen = set()
        keywords = []
        for kw in matches:
            kw_lower = kw.lower()
            if kw_lower not in seen:
                seen.add(kw_lower)
                keywords.append(kw)
        return keywords

    def _extract_images(self, content: str) -> list[dict]:
        """Extract image references from content"""
        images = []
        for match in self.image_pattern.finditer(content):
            alt_text = match.group(1)
            url = match.group(2)
            images.append({"alt": alt_text, "url": url})
        return images

    def _extract_links(self, content: str) -> list[dict]:
        """Extract links from content (excluding images)"""
        links = []
        for match in self.link_pattern.finditer(content):
            text = match.group(1)
            url = match.group(2)
            # Skip image links
            if not url.startswith(("http://", "https://")):
                continue
            links.append({"text": text, "url": url})
        return links

    def extract_chunk_metadata(
        self, chunk: "Chunk", content: str = None
    ) -> dict:
        """Extract metadata for a chunk"""
        if content is None:
            content = chunk.content

        return {
            "keywords": self._extract_keywords(content),
            "images": self._extract_images(content),
            "links": self._extract_links(content),
        }
