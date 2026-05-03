"""Prompt template manager"""

from pathlib import Path
from typing import Dict, Optional

import yaml


class PromptTemplateManager:
    """Manage prompt templates"""

    def __init__(self, templates_path: Optional[str] = None):
        self.templates: Dict[str, str] = {}
        self._load_default_templates()

        if templates_path:
            self.load_templates(templates_path)

    def _load_default_templates(self) -> None:
        """Load default prompt templates"""
        self.templates = {
            "定位指导": """你是一位昇腾AI计算平台的性能优化专家。用户遇到了性能问题，需要你提供系统化的定位指导。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 问题分析
2. 定位步骤
3. 推荐工具
4. 注意事项

回答时请引用相关文档来源，格式为【来源：文档标题】。""",

            "问题诊断": """你是一位昇腾AI计算平台的性能优化专家。用户遇到了具体的性能问题，需要你帮助诊断原因。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 问题原因分析
2. 可能的影响
3. 定位方法
4. 解决建议

回答时请引用相关文档来源，格式为【来源：文档标题】。""",

            "工具使用": """你是一位昇腾AI计算平台的性能优化专家。用户需要了解工具的使用方法。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 工具简介
2. 使用命令/步骤
3. 参数说明
4. 结果解读
5. 示例（如有）

回答时请引用相关文档来源，格式为【来源：文档标题】。""",

            "概念理解": """你是一位昇腾AI计算平台的性能优化专家。用户需要理解某个概念。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 概念定义
2. 影响说明
3. 相关场景
4. 解决方法（如适用）

回答时请引用相关文档来源，格式为【来源：文档标题】。""",

            "操作步骤": """你是一位昇腾AI计算平台的性能优化专家。用户需要了解具体的操作步骤。

用户问题：{query}

相关文档内容：
{context}

请按照以下结构回答：
1. 操作前准备
2. 详细步骤
3. 注意事项
4. 常见问题

回答时请引用相关文档来源，格式为【来源：文档标题】。""",

            "默认": """你是一位昇腾AI计算平台的性能优化专家。请根据用户问题和相关文档内容，提供专业、准确的回答。

用户问题：{query}

相关文档内容：
{context}

回答时请引用相关文档来源，格式为【来源：文档标题】。""",
        }

    def load_templates(self, path: str) -> None:
        """Load templates from YAML file"""
        template_path = Path(path)
        if template_path.exists():
            with open(template_path, encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if loaded:
                    # Convert {{var}} to {var} for Python format
                    for key, value in loaded.items():
                        self.templates[key] = value.replace("{{", "{").replace("}}", "}")

    def get_template(self, question_type: str) -> str:
        """Get template for question type"""
        return self.templates.get(question_type, self.templates["默认"])

    def render(
        self,
        question_type: str,
        query: str,
        context: str,
    ) -> str:
        """Render prompt with query and context"""
        template = self.get_template(question_type)
        return template.format(query=query, context=context)

    def add_template(self, name: str, template: str) -> None:
        """Add a new template"""
        self.templates[name] = template

    def list_templates(self) -> list:
        """List available templates"""
        return list(self.templates.keys())