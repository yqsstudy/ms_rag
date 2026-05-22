"""Text cleaner for document preprocessing"""

import re
from typing import Optional


class TextCleaner:
    """Clean text content"""

    def __init__(
        self,
        remove_html: bool = True,
        normalize_whitespace: bool = True,
        remove_empty_lines: bool = True,
    ):
        self.remove_html = remove_html
        self.normalize_whitespace = normalize_whitespace
        self.remove_empty_lines = remove_empty_lines

        # Patterns for cleaning
        self.style_script_pattern = re.compile(r"<(style|script)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
        self.html_pattern = re.compile(r"<(?!/?(?:table|thead|tbody|tr|th|td)[> ])[^>]+>", re.IGNORECASE)
        self.whitespace_pattern = re.compile(r"[ \t]+")
        self.empty_line_pattern = re.compile(r"\n\s*\n+")
        self.special_chars_pattern = re.compile(r"[^\w\s\u4e00-\u9fff\-.,!?;:\"\'()（）【】「」《》]")

    def clean(self, text: str) -> str:
        """Clean text content"""
        if self.remove_html:
            text = self._remove_html_tags(text)

        if self.normalize_whitespace:
            text = self._normalize_whitespace(text)

        if self.remove_empty_lines:
            text = self._remove_empty_lines(text)

        return text.strip()

    def _remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text"""
        text = self.style_script_pattern.sub("", text)
        return self.html_pattern.sub("", text)

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text"""
        # Replace multiple spaces/tabs with single space
        text = self.whitespace_pattern.sub(" ", text)
        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return text

    def _remove_empty_lines(self, text: str) -> str:
        """Remove excessive empty lines"""
        # Replace multiple empty lines with single empty line
        return self.empty_line_pattern.sub("\n\n", text)

    def clean_chunk_content(self, content: str) -> str:
        """Clean chunk content while preserving structure"""
        # Remove source link lines (they're metadata, not content)
        content = re.sub(r"^> 来源:.*$", "", content, flags=re.MULTILINE)

        # Remove excessive markdown formatting
        content = re.sub(r"\*{3,}", "---", content)  # Horizontal rules
        content = re.sub(r"_{3,}", "---", content)

        # Clean table formatting (preserve structure)
        content = re.sub(r"\|\s{2,}", "| ", content)

        # Apply standard cleaning
        return self.clean(content)