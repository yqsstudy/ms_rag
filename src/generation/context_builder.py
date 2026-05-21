"""Context builder for LLM input"""

from typing import List

from ..retrieval.hybrid_retriever import HybridResult


class ContextBuilder:
    """Build context for LLM from search results"""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        # Approximate tokens per character for Chinese
        self.chars_per_token = 2

    def build_context(
        self,
        results: List[HybridResult],
        max_chunks: int = 5,
    ) -> str:
        """Build context string from search results"""
        context_parts = []
        current_chars = 0
        max_chars = self.max_tokens * self.chars_per_token

        seen_docs = {}
        doc_counter = 1

        for result in results[:max_chunks]:
            if result.doc_id not in seen_docs:
                seen_docs[result.doc_id] = doc_counter
                doc_counter += 1
                
            doc_index = seen_docs[result.doc_id]
            chunk_text = self._format_chunk(result, doc_index)
            chunk_chars = len(chunk_text)

            if current_chars + chunk_chars > max_chars:
                # Truncate if needed
                remaining_chars = max_chars - current_chars
                if remaining_chars > 200:  # Only add if meaningful
                    chunk_text = chunk_text[:remaining_chars] + "..."
                    context_parts.append(chunk_text)
                break

            context_parts.append(chunk_text)
            current_chars += chunk_chars

        return "\n\n---\n\n".join(context_parts)

    def _format_chunk(self, result: HybridResult, index: int) -> str:
        """Format a single chunk for context"""
        # 基础信息
        chunk_text = f"""【文档{index}】{result.doc_title}
【章节】{result.section_title}
【内容】{result.content}
【来源】{result.source_url}"""

        # 如果有图片，添加图片描述
        if result.images:
            images_text = "\n【相关图片】"
            for img in result.images:
                if img.get("figure_num"):
                    images_text += f"\n  图{img['figure_num']}: {img.get('caption', '未命名')}"
                else:
                    images_text += f"\n  {img.get('caption', '未命名图片')}"
            chunk_text += images_text

        return chunk_text

    def build_sources(self, results: List[HybridResult]) -> List[dict]:
        """Build source list for response"""
        sources = []
        seen_docs = set()

        for result in results:
            if result.doc_id not in seen_docs:
                source = {
                    "doc_id": result.doc_id,
                    "title": result.doc_title,
                    "section": result.section_title,
                    "source_url": result.source_url,
                    "relevance_score": round(result.final_score, 3),
                }

                # 添加图片信息
                if result.images:
                    source["images"] = [
                        {
                            "figure_num": img.get("figure_num"),
                            "caption": img.get("caption"),
                            "path": img.get("path"),
                        }
                        for img in result.images
                    ]

                sources.append(source)
                seen_docs.add(result.doc_id)

        return sources[:5]  # Limit to top 5 unique documents