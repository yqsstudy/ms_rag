"""Document loader for corpus files"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Document:
    """Document data class"""

    doc_id: str
    title: str
    content: str
    source_url: str
    file_path: str
    date_collected: Optional[str] = None
    parent_topic: Optional[str] = None
    file_hash: Optional[str] = None


class DocumentLoader:
    """Load documents from corpus directory"""

    def __init__(self, corpus_path: str):
        self.corpus_path = Path(corpus_path)
        self.frontmatter_pattern = re.compile(
            r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL
        )

    def load_document(self, file_path: Path) -> Document:
        """Load a single document from file"""
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Parse YAML frontmatter
        frontmatter = {}
        match = self.frontmatter_pattern.match(content)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                content = content[match.end() :]
            except yaml.YAMLError:
                pass

        try:
            rel_path = file_path.relative_to(self.corpus_path)
            doc_id = str(rel_path.with_suffix("")).replace("/", "_").replace("\\", "_")
        except ValueError:
            doc_id = file_path.stem

        import hashlib
        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        title = frontmatter.get("title", doc_id)
        source_url = frontmatter.get("source", "")
        if source_url.startswith("msinsight-docs://"):
            search_query = title.strip("*")
            import urllib.parse
            source_url = f"https://www.hiascend.com/search?q={urllib.parse.quote(search_query)}"

        return Document(
            doc_id=doc_id,
            title=title,
            content=content.strip(),
            source_url=source_url,
            file_path=str(file_path),
            date_collected=frontmatter.get("date_collected"),
            parent_topic=self._extract_parent_topic(content),
            file_hash=file_hash,
        )

    def _extract_parent_topic(self, content: str) -> Optional[str]:
        """Extract parent topic doc_id from document content"""
        # Pattern: **父主题：** [title](url) or 父主题：[title](url)
        match = re.search(r"父主题[：:]\s*\*?\*?\s*\[([^\]]+)\]\(([^)]+)\)", content)
        if match:
            url = match.group(2)
            doc_id_match = re.search(r"([^/]+)(?:\.md|\.html)$", url)
            if doc_id_match:
                return doc_id_match.group(1).replace(".md", "").replace(".html", "")
        # Fallback: plain text parent topic
        match = re.search(r"父主题[：:]\s*\*?\*?\s*(\S+)", content)
        if match:
            text = match.group(1).strip("*")
            if text and not text.startswith("http"):
                return text
        return None

    def load_all_documents(self) -> list[Document]:
        """Load all documents from corpus directory"""
        documents = []

        for file_path in self.corpus_path.rglob("*.md"):
            if file_path.name in ["README.md", "STRUCTURE.md"]:
                continue

            try:
                doc = self.load_document(file_path)
                documents.append(doc)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        return documents

    def get_document_count(self) -> int:
        """Get total number of documents"""
        return len([f for f in self.corpus_path.rglob("*.md")
                   if f.name not in ["README.md", "STRUCTURE.md"]])
