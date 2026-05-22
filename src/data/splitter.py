"""Document splitter for chunking"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    """Chunk data class"""

    chunk_id: str
    doc_id: str
    doc_title: str
    section_title: str
    content: str
    source_url: str
    parent_topic: Optional[str] = None
    images: list[dict] = field(default_factory=list)  # 改为dict列表
    keywords: list[str] = field(default_factory=list)
    parent_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "doc_title": self.doc_title,
            "section_title": self.section_title,
            "content": self.content,
            "source_url": self.source_url,
            "parent_topic": self.parent_topic,
            "images": self.images,
            "keywords": self.keywords,
            "parent_id": self.parent_id,
        }


@dataclass
class ChunkingConfig:
    """Chunking configuration"""

    min_chunk_size: int = 1500
    max_chunk_size: int = 2000
    chunk_overlap: int = 200
    child_chunk_size: int = 400
    child_chunk_overlap: int = 50
    heading_patterns: list[str] = field(
        default_factory=lambda: [r"^#{1,4}\s+", r"^#+\s+"]
    )


class DocumentSplitter:
    """Split documents into chunks"""

    def __init__(self, config: Optional[ChunkingConfig] = None):
        self.config = config or ChunkingConfig()
        self.heading_pattern = re.compile(r"^(#{1,4})\s+(.+)$", re.MULTILINE)

    def split_document(self, doc: "Document") -> list[Chunk]:
        """Split a document into chunks"""
        # Find all section headings
        sections = self._find_sections(doc.content)

        chunks = []
        for i, (title, content, start_pos) in enumerate(sections):
            # Handle long sections
            if len(content) > self.config.max_chunk_size:
                sub_chunks = self._split_long_section(
                    content, doc, title, i
                )
                chunks.extend(sub_chunks)
            else:
                chunk_id = f"{doc.doc_id}_chunk_{i}"
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        doc_id=doc.doc_id,
                        doc_title=doc.title,
                        section_title=title,
                        content=content.strip(),
                        source_url=doc.source_url,
                        parent_topic=doc.parent_topic,
                        images=self._extract_images(content),
                    )
                )

        # Handle very short documents - keep as single chunk
        if not chunks and len(doc.content) > 0:
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}_chunk_0",
                    doc_id=doc.doc_id,
                    doc_title=doc.title,
                    section_title=doc.title,
                    content=doc.content.strip(),
                    source_url=doc.source_url,
                    parent_topic=doc.parent_topic,
                    images=self._extract_images(doc.content),
                )
            )

        # Add overlap between consecutive chunks
        chunks = self._add_overlap(chunks)

        return chunks

    def split_into_children(self, parent: Chunk) -> list[Chunk]:
        child_chunks = []
        content = parent.content
        child_size = getattr(self.config, 'child_chunk_size', 400)
        overlap = getattr(self.config, 'child_chunk_overlap', 50)
        
        start = 0
        idx = 0
        while start < len(content):
            end = start + child_size
            
            if end < len(content):
                for offset in range(0, min(100, end - start)):
                    if content[end - offset - 1] in "。！？\n":
                        end = end - offset
                        break
                        
            chunk_content = content[start:end]
            if chunk_content.strip():
                child = Chunk(
                    chunk_id=f"{parent.chunk_id}_child_{idx}",
                    doc_id=parent.doc_id,
                    doc_title=parent.doc_title,
                    section_title=parent.section_title,
                    content=chunk_content.strip(),
                    source_url=parent.source_url,
                    parent_topic=parent.parent_topic,
                    images=parent.images,
                    parent_id=parent.chunk_id
                )
                child_chunks.append(child)
                idx += 1
                
            start = end - overlap
            if start <= 0 or start >= len(content) - overlap:
                start = end
                
        if not child_chunks:
            child = Chunk(
                chunk_id=f"{parent.chunk_id}_child_0",
                doc_id=parent.doc_id,
                doc_title=parent.doc_title,
                section_title=parent.section_title,
                content=parent.content,
                source_url=parent.source_url,
                parent_topic=parent.parent_topic,
                images=parent.images,
                parent_id=parent.chunk_id
            )
            child_chunks.append(child)
            
        return child_chunks

    def _add_overlap(self, chunks: list[Chunk]) -> list[Chunk]:
        """Add overlap content between consecutive chunks"""
        if len(chunks) <= 1 or self.config.chunk_overlap <= 0:
            return chunks

        result = []
        for i, chunk in enumerate(chunks):
            content = chunk.content

            # Add suffix from previous chunk
            if i > 0:
                prev_content = chunks[i - 1].content
                # Get last N characters from previous chunk
                overlap_text = self._get_overlap_text(prev_content, from_end=True)
                if overlap_text:
                    content = overlap_text + "\n\n" + content

            # Add prefix from next chunk
            if i < len(chunks) - 1:
                next_content = chunks[i + 1].content
                # Get first N characters from next chunk
                overlap_text = self._get_overlap_text(next_content, from_end=False)
                if overlap_text:
                    content = content + "\n\n" + overlap_text

            # Create new chunk with overlap
            result.append(
                Chunk(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    doc_title=chunk.doc_title,
                    section_title=chunk.section_title,
                    content=content.strip(),
                    source_url=chunk.source_url,
                    parent_topic=chunk.parent_topic,
                    images=chunk.images,
                    keywords=chunk.keywords,
                )
            )

        return result

    def _get_overlap_text(self, content: str, from_end: bool = True) -> str:
        """Get overlap text from content

        Args:
            content: The content to extract from
            from_end: If True, get from end; if False, get from beginning

        Returns:
            Overlap text, trying to break at sentence/paragraph boundaries
        """
        if len(content) <= self.config.chunk_overlap:
            return content

        if from_end:
            # Get last N characters
            text = content[-self.config.chunk_overlap:]
            # Try to find a good break point (paragraph or sentence)
            # Look for paragraph break first
            para_break = text.find("\n\n")
            if para_break > 0:
                text = text[para_break + 2:]
            else:
                # Try sentence break (。！？)
                for i, char in enumerate(text):
                    if char in "。！？\n":
                        text = text[i + 1:]
                        break
        else:
            # Get first N characters
            text = content[:self.config.chunk_overlap]
            # Try to find a good break point
            # Look for paragraph break from end
            para_break = text.rfind("\n\n")
            if para_break > 0:
                text = text[:para_break]
            else:
                # Try sentence break from end
                for i in range(len(text) - 1, -1, -1):
                    if text[i] in "。！？\n":
                        text = text[:i + 1]
                        break

        return text.strip()

    def _find_sections(self, content: str) -> list[tuple[str, str, int]]:
        """Find all sections in document content"""
        sections = []
        matches = list(self.heading_pattern.finditer(content))

        if not matches:
            # No headings, return entire content
            return [("正文", content, 0)]

        # Add content before first heading
        if matches[0].start() > 0:
            sections.append(("正文", content[: matches[0].start()], 0))

        # Add each section
        hierarchy = []
        for i, match in enumerate(matches):
            level = len(match.group(1))
            title_text = match.group(2).strip()
            
            hierarchy = [h for h in hierarchy if h[0] < level]
            hierarchy.append((level, title_text))
            
            full_title = " > ".join([h[1] for h in hierarchy])

            start = match.end()

            # Find end of section (next heading or end of content)
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(content)

            section_content = content[start:end]
            sections.append((full_title, section_content, match.start()))

        return sections

    def _split_long_section(
        self, content: str, doc: "Document", section_title: str, section_idx: int
    ) -> list[Chunk]:
        chunks = []
        protected_ranges = []
        
        for match in re.finditer(r"```.*?```", content, re.DOTALL):
            protected_ranges.append((match.start(), match.end()))
            
        for match in re.finditer(r"<table.*?>.*?</table>", content, re.DOTALL | re.IGNORECASE):
            protected_ranges.append((match.start(), match.end()))
            
        protected_ranges.sort(key=lambda x: x[0])
        
        merged_ranges = []
        for r in protected_ranges:
            if not merged_ranges:
                merged_ranges.append(r)
            else:
                last = merged_ranges[-1]
                if r[0] <= last[1]:
                    merged_ranges[-1] = (last[0], max(last[1], r[1]))
                else:
                    merged_ranges.append(r)

        paragraphs = []
        last_end = 0
        
        for match in re.finditer(r"\n\n+", content):
            split_pos = match.start()
            
            is_protected = False
            for r_start, r_end in merged_ranges:
                if r_start < split_pos < r_end:
                    is_protected = True
                    break
                    
            if not is_protected:
                para = content[last_end:split_pos]
                if para.strip():
                    paragraphs.append(para)
                last_end = match.end()
                
        if last_end < len(content):
            para = content[last_end:]
            if para.strip():
                paragraphs.append(para)

        if not paragraphs:
            paragraphs = [content]

        current_chunk = ""
        chunk_idx = 0

        for para in paragraphs:
            if len(current_chunk) + len(para) > self.config.max_chunk_size:
                if current_chunk:
                    chunk_id = f"{doc.doc_id}_chunk_{section_idx}_{chunk_idx}"
                    chunks.append(
                        Chunk(
                            chunk_id=chunk_id,
                            doc_id=doc.doc_id,
                            doc_title=doc.title,
                            section_title=f"{section_title} ({chunk_idx + 1})",
                            content=current_chunk.strip(),
                            source_url=doc.source_url,
                            parent_topic=doc.parent_topic,
                            images=self._extract_images(current_chunk),
                        )
                    )
                    chunk_idx += 1
                    current_chunk = para
                else:
                    chunk_id = f"{doc.doc_id}_chunk_{section_idx}_{chunk_idx}"
                    chunks.append(
                        Chunk(
                            chunk_id=chunk_id,
                            doc_id=doc.doc_id,
                            doc_title=doc.title,
                            section_title=f"{section_title} ({chunk_idx + 1})",
                            content=para.strip(),
                            source_url=doc.source_url,
                            parent_topic=doc.parent_topic,
                            images=self._extract_images(para),
                        )
                    )
                    chunk_idx += 1
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para

        if current_chunk:
            chunk_id = f"{doc.doc_id}_chunk_{section_idx}_{chunk_idx}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc.doc_id,
                    doc_title=doc.title,
                    section_title=f"{section_title} ({chunk_idx + 1})",
                    content=current_chunk.strip(),
                    source_url=doc.source_url,
                    parent_topic=doc.parent_topic,
                    images=self._extract_images(current_chunk),
                )
            )

        return chunks

    def _extract_images(self, content: str) -> list[dict]:
        """Extract image references from content

        匹配两种格式：
        1. **图X** 标题 后面跟着 ![](path)
        2. 单独的 ![alt](path)
        """
        images = []

        # 模式1: **图X** 标题 后面跟着图片
        # 例如: **图1** 详细排查流程图
        #       ![](images/xxx.jpg)
        figure_pattern = r'\*\*图(\d+)\*\*\s*([^\n]+?)\s*\n(?:<[^>]*>|\s)*!\[[^\]]*\]\(([^)]+)\)'

        for match in re.finditer(figure_pattern, content):
            images.append({
                "figure_num": match.group(1),
                "caption": match.group(2).strip(),
                "path": match.group(3),
            })

        # 模式2: 单独的图片，没有图X标题
        # 例如: ![描述](images/xxx.png)
        simple_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        for match in re.finditer(simple_pattern, content):
            alt = match.group(1).strip()
            path = match.group(2)

            # 检查是否已经被模式1匹配
            if any(img["path"] == path for img in images):
                continue

            # 只保留有描述的图片
            if alt:
                images.append({
                    "figure_num": None,
                    "caption": alt,
                    "path": path,
                })

        return images
