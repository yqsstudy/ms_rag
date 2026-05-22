"""Prompt templates for RAG eval dataset generation."""

GENERATE_QUESTIONS_SYSTEM = """你是 RAG 评测数据集构造助手。你只能根据给定技术文档片段生成问题，不要引入文档外知识。输出必须是严格 JSON。"""

GENERATE_QUESTIONS_USER = """请基于下面的技术文档片段生成 {questions_per_chunk} 个高质量评测问题。

要求：
1. 问题必须能由该片段或其直接上下文回答。
2. 避免过宽泛问题，例如“如何进行性能优化”。
3. 问题要贴近真实用户的理解、使用或排障场景。
4. question_type 只能从以下值选择：{allowed_types}
5. difficulty 只能是 easy、medium、hard。
6. 输出严格 JSON 数组，不要输出解释文字。

文档标题：{doc_title}
章节：{section_title}
来源：{source_file}

文档片段：
{content}

输出格式：
[
  {{
    "question": "...",
    "question_type": "troubleshooting",
    "difficulty": "medium",
    "keywords": ["关键词1", "关键词2"]
  }}
]
"""

GENERATE_SECTION_QUESTIONS_SYSTEM = """你是 RAG 评测数据集构造助手。你只能根据给定技术文档章节生成问题，不要引入文档外知识。输出必须是严格 JSON。"""

GENERATE_SECTION_QUESTIONS_USER = """请基于下面的技术文档章节生成 {questions_per_item} 个章节级评测问题。

要求：
1. 问题应围绕该章节的主题、流程、适用条件、参数含义或排障入口。
2. 问题必须能由该章节内的多个片段共同回答，避免只考察单句细节。
3. 问题要贴近真实用户会如何询问该章节内容。
4. question_type 只能从以下值选择：{allowed_types}
5. difficulty 只能是 easy、medium、hard。
6. 输出严格 JSON 数组，不要输出解释文字。

文档标题：{doc_title}
章节：{section_title}
章节路径：{section_path}
来源：{source_file}

章节代表片段：
{content}

输出格式：
[
  {{
    "question": "...",
    "question_type": "how_to",
    "difficulty": "medium",
    "keywords": ["关键词1", "关键词2"]
  }}
]
"""

GENERATE_DOCUMENT_QUESTIONS_SYSTEM = """你是 RAG 评测数据集构造助手。你只能根据给定技术文档概要生成问题，不要引入文档外知识。输出必须是严格 JSON。"""

GENERATE_DOCUMENT_QUESTIONS_USER = """请基于下面的技术文档概要生成 {questions_per_item} 个文档级评测问题。

要求：
1. 问题应覆盖文档整体主题，例如工具用途、完整流程、典型场景、限制条件或排障思路。
2. 问题应比单个片段更高层，但不能宽泛到脱离该文档。
3. 问题要像真实用户在不知道具体章节时提出的入口型问题。
4. question_type 只能从以下值选择：{allowed_types}
5. difficulty 只能是 easy、medium、hard。
6. 输出严格 JSON 数组，不要输出解释文字。

文档标题：{doc_title}
章节列表：{section_titles}
来源：{source_file}

文档代表片段：
{content}

输出格式：
[
  {{
    "question": "...",
    "question_type": "concept",
    "difficulty": "medium",
    "keywords": ["关键词1", "关键词2"]
  }}
]
"""

JUDGE_EVIDENCE_SYSTEM = """你是 RAG 评测证据标注助手。你只判断候选片段是否能支持回答问题，不生成最终答案，不使用外部知识。输出必须是严格 JSON。"""

JUDGE_EVIDENCE_USER = """请判断下面 evidence cards 是否支持回答用户问题。

相关性等级：
0 = 无关
1 = 主题相关但不能回答问题
2 = 部分支持回答
3 = 直接支持回答

用户问题：{question}

Evidence Cards:
{cards_json}

输出严格 JSON：
{{
  "judged_chunks": [
    {{
      "chunk_id": "...",
      "relevance": 0,
      "supported_points": ["..."],
      "reason": "简短原因"
    }}
  ]
}}
"""

SYNTHESIZE_ANSWER_SYSTEM = """你是 RAG 评测标准答案构造助手。你只能基于 supporting chunks 归纳答案要点，不要引入文档外知识。输出必须是严格 JSON。"""

SYNTHESIZE_ANSWER_USER = """请基于 supporting chunks 为用户问题构造评测样本。

要求：
1. 如果证据不足以回答问题，设置 is_answerable=false。
2. answer_key_points 每条要点尽量绑定 supporting chunk。
3. must_have_points 是判断答案是否完整的核心要点，数量控制在 {max_must_have_points} 条以内。
4. nice_to_have_points 是加分要点，数量控制在 {max_nice_to_have_points} 条以内。
5. 不要使用文档外知识。
6. 输出严格 JSON。

用户问题：{question}
问题类型：{question_type}
难度：{difficulty}
关键词：{keywords}

Supporting Chunks:
{chunks_json}

输出格式：
{{
  "is_answerable": true,
  "answer_key_points": [
    {{"point": "...", "supporting_chunks": ["chunk_id"]}}
  ],
  "must_have_points": ["..."],
  "nice_to_have_points": ["..."],
  "expected_answer": "...",
  "acceptable_chunk_ids": ["..."],
  "acceptable_source_files": ["..."],
  "conflicts": []
}}
"""
