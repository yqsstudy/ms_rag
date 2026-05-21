#!/usr/bin/env python3
"""
MindStudio 文档爬取脚本
从 hiascend.com 爬取文档并转换为 RAG 语料格式。
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from datetime import date

BASE_URL = "https://www.hiascend.com"
DOC_SOURCE_URL = f"{BASE_URL}/doc_center/source"
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# Icon size threshold
ICON_SIZE_THRESHOLD = 5000


class HTMLToMarkdown(HTMLParser):
    """Convert HTML to Markdown, extracting main content."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.current_tag = None
        self.tag_stack = []
        self.in_content = False
        self.in_table = False
        self.table_rows = []
        self.current_row = []
        self.current_cell = []
        self.in_code = False
        self.code_content = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.skip_depth = 0
        self.in_pre = False
        self.list_stack = []  # stack of ('ul' or 'ol', counter)
        self.current_text = ''
        self.td_is_header = False
        self.href_stack = []
        self.img_list = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in self.skip_tags:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return

        self.tag_stack.append(tag)

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._flush_text()
            level = int(tag[1])
            self.result.append('\n' + '#' * level + ' ')

        elif tag == 'p':
            self._flush_text()
            self.result.append('\n')

        elif tag == 'br':
            self.result.append('\n')

        elif tag == 'table':
            self._flush_text()
            self.in_table = True
            self.table_rows = []

        elif tag == 'tr' and self.in_table:
            self.current_row = []

        elif tag in ('td', 'th') and self.in_table:
            self.current_cell = []
            self.td_is_header = (tag == 'th')

        elif tag == 'pre':
            self._flush_text()
            self.in_pre = True
            self.code_content = []

        elif tag == 'code':
            if not self.in_pre:
                self.result.append('`')
            self.in_code = True
            self.code_content = []

        elif tag == 'ul':
            self._flush_text()
            self.list_stack.append(('ul', 0))

        elif tag == 'ol':
            self._flush_text()
            self.list_stack.append(('ol', 0))

        elif tag == 'li':
            self._flush_text()
            indent = '  ' * (len(self.list_stack) - 1)
            if self.list_stack:
                list_type, counter = self.list_stack[-1]
                if list_type == 'ol':
                    self.list_stack[-1] = (list_type, counter + 1)
                    self.result.append(f'\n{indent}{counter + 1}. ')
                else:
                    self.result.append(f'\n{indent}- ')
            else:
                self.result.append(f'\n- ')

        elif tag == 'a':
            href = attrs_dict.get('href', '')
            if href and not href.startswith('#') and not href.startswith('javascript'):
                self.href_stack.append(href)
                self.result.append('[')
            else:
                self.href_stack.append('')

        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            title = attrs_dict.get('title', '')
            if src:
                self.img_list.append(src)
                if title:
                    self.result.append(f'![{alt}]({src} "{title}")')
                else:
                    self.result.append(f'![{alt}]({src})')

        elif tag == 'strong' or tag == 'b':
            self.result.append('**')

        elif tag == 'em' or tag == 'i':
            self.result.append('*')

        elif tag == 'blockquote':
            self._flush_text()
            self.result.append('\n> ')

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth -= 1
            return
        if self.skip_depth > 0:
            return

        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._flush_text()
            self.result.append('\n')

        elif tag == 'p':
            self._flush_text()
            self.result.append('\n')

        elif tag == 'table':
            self._flush_text()
            if self.table_rows:
                self._render_table()
            self.in_table = False
            self.table_rows = []

        elif tag == 'tr' and self.in_table:
            if self.current_row:
                self.table_rows.append(self.current_row)

        elif tag in ('td', 'th') and self.in_table:
            cell_text = ''.join(self.current_cell).strip()
            cell_text = re.sub(r'\s+', ' ', cell_text)
            self.current_row.append(cell_text)

        elif tag == 'pre':
            code = ''.join(self.code_content)
            self.result.append(f'\n```\n{code}\n```\n')
            self.in_pre = False
            self.code_content = []

        elif tag == 'code':
            if self.in_pre:
                pass  # handled in pre end
            else:
                code = ''.join(self.code_content)
                self.result.append(f'{code}`')
            self.in_code = False
            self.code_content = []

        elif tag in ('ul', 'ol'):
            self._flush_text()
            if self.list_stack:
                self.list_stack.pop()
            self.result.append('\n')

        elif tag == 'li':
            self._flush_text()

        elif tag == 'a':
            self._flush_text()
            href = self.href_stack.pop() if self.href_stack else ''
            if href:
                self.result.append(f']({href})')

        elif tag == 'strong' or tag == 'b':
            self._flush_text()
            self.result.append('**')

        elif tag == 'em' or tag == 'i':
            self._flush_text()
            self.result.append('*')

    def handle_data(self, data):
        if self.skip_depth > 0:
            return

        if self.in_pre or self.in_code:
            self.code_content.append(data)
            return

        if self.in_table and self.tag_stack and self.tag_stack[-1] in ('td', 'th'):
            self.current_cell.append(data)
            return

        self.current_text += data

    def _flush_text(self):
        if self.current_text:
            text = self.current_text
            # Normalize whitespace but preserve single newlines
            text = re.sub(r'[ \t]+', ' ', text)
            text = text.strip()
            if text:
                self.result.append(text)
            self.current_text = ''

    def _render_table(self):
        if not self.table_rows:
            return
        # Find max columns
        max_cols = max(len(row) for row in self.table_rows)
        # Pad rows
        for row in self.table_rows:
            while len(row) < max_cols:
                row.append('')

        # Header
        header = self.table_rows[0]
        self.result.append('| ' + ' | '.join(header) + ' |\n')
        self.result.append('| ' + ' | '.join(['---'] * max_cols) + ' |\n')

        # Body
        for row in self.table_rows[1:]:
            self.result.append('| ' + ' | '.join(row) + ' |\n')

    def get_markdown(self):
        self._flush_text()
        text = ''.join(self.result)
        # Clean up multiple blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def get_images(self):
        return self.img_list


def fetch_page(page_path, retries=3):
    """Fetch a page's HTML content from the doc center."""
    url = f"{DOC_SOURCE_URL}/{page_path}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1 * (attempt + 1))
            else:
                print(f"  ERROR fetching {page_path}: {e}")
                return None


def fetch_breadcrumbs(page_path):
    """Fetch breadcrumbs to get next page URL."""
    api_path = page_path.replace('.html', '_90x_html')
    url = f"{BASE_URL}/ascendgateway/ascendservice/doc/page/breadcrumbs/{api_path}"
    try:
        req = urllib.request.Request(url, headers={
            **HEADERS,
            'Referer': f'{BASE_URL}/document/detail/{page_path}',
            'Accept': 'application/json',
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('success') and data.get('data'):
                return data['data']
    except Exception as e:
        pass
    return None


def enumerate_section(start_path, max_pages=300):
    """Enumerate all pages in a section by following next links."""
    pages = []
    current = start_path
    visited = set()

    while current and len(pages) < max_pages:
        if current in visited:
            break
        visited.add(current)

        data = fetch_breadcrumbs(current)
        if not data:
            # Fallback: just use the start page
            if not pages:
                pages.append({'name': 'index', 'url': current})
            break

        pages.append({
            'name': data.get('finalNodeName', ''),
            'url': data.get('finalNodeUrl', ''),
        })

        next_url = data.get('nextNodeUrl')
        if next_url and next_url != current:
            current = next_url
        else:
            break

    return pages


def download_image(img_url, images_dir, used_names):
    """Download an image and return the local filename."""
    # Make absolute URL
    if img_url.startswith('/'):
        full_url = BASE_URL + img_url
    elif img_url.startswith('http'):
        full_url = img_url
    else:
        # Relative URL - skip for now
        return None

    # Generate filename from URL
    url_hash = hashlib.md5(full_url.encode()).hexdigest()[:8]
    ext = os.path.splitext(urllib.parse.urlparse(full_url).path)[1] or '.png'
    # Clean extension
    ext = ext.split('?')[0]
    if ext not in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'):
        ext = '.png'

    # Try to use original name
    orig_name = os.path.basename(urllib.parse.urlparse(full_url).path).split('?')[0]
    if orig_name and orig_name not in used_names:
        name = orig_name
    else:
        name = f"img_{url_hash}{ext}"
        # Avoid collisions
        while name in used_names:
            url_hash += 'x'
            name = f"img_{url_hash}{ext}"

    used_names.add(name)
    dest = images_dir / name

    if dest.exists():
        return name

    try:
        req = urllib.request.Request(full_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            # Skip tiny icons
            if len(data) < ICON_SIZE_THRESHOLD:
                return None
            dest.write_bytes(data)
            return name
    except Exception as e:
        return None


def html_to_markdown(html_content):
    """Convert HTML to Markdown."""
    parser = HTMLToMarkdown()
    parser.feed(html_content)
    return parser.get_markdown(), parser.get_images()


def extract_title_from_html(html_content):
    """Extract title from HTML."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if title:
            return title
    m = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return ''


def process_page(page_info, corpus_dir, images_dir, used_img_names, section_name):
    """Process a single page: fetch, convert, save."""
    page_path = page_info['url']
    page_name = page_info['name']

    # Fetch HTML
    html = fetch_page(page_path)
    if not html:
        return None

    # Extract title
    title = extract_title_from_html(html) or page_name

    # Convert to Markdown
    md_content, img_refs = html_to_markdown(html)

    if not md_content or len(md_content.strip()) < 50:
        return None

    # Download images and update references
    img_mapping = {}
    for img_ref in img_refs:
        local_name = download_image(img_ref, images_dir, used_img_names)
        if local_name:
            img_mapping[img_ref] = local_name

    # Update image paths in markdown
    for old_ref, new_name in img_mapping.items():
        md_content = md_content.replace(old_ref, f'images/{new_name}')

    # Remove references to images we couldn't download
    for img_ref in img_refs:
        if img_ref not in img_mapping:
            md_content = re.sub(r'!\[[^\]]*\]\(' + re.escape(img_ref) + r'\)', '', md_content)

    # Generate filename from page path
    # e.g., zh/mindstudio/830/ODtools/.../atlasopdev_16_0005.html -> atlasopdev_16_0005
    stem = Path(page_path).stem
    # Sanitize
    safe_stem = re.sub(r'[^a-zA-Z0-9_-]', '_', stem)
    corpus_filename = f"{safe_stem}.md"

    # Build frontmatter
    source_url = f"{BASE_URL}/document/detail/{page_path}"
    frontmatter = f"""---
title: "{title}"
source: "{source_url}"
date_collected: "{date.today().isoformat()}"
category: "{section_name}"
original_path: "{page_path}"
---

"""

    # Write file
    out_path = corpus_dir / corpus_filename
    out_path.write_text(frontmatter + md_content, encoding='utf-8')

    return out_path


def crawl_section(section_name, start_path, corpus_base, crawl_plan_data=None):
    """Crawl an entire section."""
    corpus_dir = corpus_base / section_name
    images_dir = corpus_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Enumerate pages
    print(f"\n{'='*60}")
    print(f"开始爬取: {section_name}")
    print(f"起始页面: {start_path}")
    print(f"输出目录: {corpus_dir}")

    if isinstance(crawl_plan_data, list):
        pages = crawl_plan_data
        print(f"从计划数据加载 {len(pages)} 页")
    elif isinstance(crawl_plan_data, dict) and section_name in crawl_plan_data:
        pages = crawl_plan_data[section_name]
        print(f"从计划数据加载 {len(pages)} 页")
    else:
        print("枚举页面...")
        pages = enumerate_section(start_path)
        print(f"枚举完成: {len(pages)} 页")

    used_img_names = set()
    success = 0
    failed = 0

    for i, page in enumerate(pages):
        page_url = page.get('url', page) if isinstance(page, dict) else page
        page_name = page.get('name', '') if isinstance(page, dict) else ''

        print(f"  [{i+1}/{len(pages)}] {page_name or page_url}...", end=' ', flush=True)

        result = process_page(
            {'name': page_name, 'url': page_url},
            corpus_dir, images_dir, used_img_names, section_name
        )

        if result:
            print(f"OK ({result.name})")
            success += 1
        else:
            print("SKIP")
            failed += 1

        # Rate limiting
        time.sleep(0.3)

    print(f"\n完成: {success} 成功, {failed} 跳过")
    print(f"图片: {len(list(images_dir.iterdir()))} 张")

    # Save page list for reference
    manifest = {
        'section': section_name,
        'total_pages': len(pages),
        'success': success,
        'failed': failed,
        'pages': pages,
    }
    with open(corpus_dir / '_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return success


def main():
    parser = argparse.ArgumentParser(description="Crawl MindStudio docs")
    parser.add_argument('--section', help='Section name to crawl (or "all" for P0)')
    parser.add_argument('--corpus-base', default='./corpus', help='Base corpus directory')
    parser.add_argument('--plan', default='./docs/mindstudio_crawl_plan_data.json',
                        help='Path to crawl plan data JSON')
    args = parser.parse_args()

    corpus_base = Path(args.corpus_base)

    # Load crawl plan if available
    crawl_plan_data = {}
    plan_path = Path(args.plan)
    if plan_path.exists():
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)
            for section_name, pages in plan.get('sections', {}).items():
                crawl_plan_data[section_name] = pages

    # Define all sections: section_key -> (display_name, start_path, plan_data_keys)
    # plan_data_keys: list of keys in crawl_plan_data to merge, or None for direct match
    all_sections = {
        # P0
        'operator_tools': ('算子开发工具', 'zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0005.html', None),
        'profiling_tools': ('性能调优工具', 'zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html', None),
        'accuracy_tools': ('精度调试工具', 'zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html', None),
        # P1
        'quickstart': ('快速入门', 'zh/mindstudio/830/msquickstart/tools_qucikstart_0001.html', None),
        'llm_cases': ('大模型相关案例', 'zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_001.html', [
            '大模型训练精度问题定位案例',
            '大模型推理精度问题分析案例',
            '大模型训练性能瓶颈定位流程案例',
            '大模型推理量化调试调优指南',
            '传统模型推理迁移调试调优全流程指南',
            '内存问题分析案例',
        ]),
        # P2
        'msleaks': ('msLeaks内存泄漏检测工具', 'zh/mindstudio/830/T&ITools/msleaks/atlasmsleaks_16_0001.html', None),
        'migration_tools': ('分析迁移工具', 'zh/mindstudio/830/T&ITools/MigrationTools/atlasgratlas_16_0001.html', None),
        'mstx_api': ('mstx API参考', 'zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html', None),
        # P3
        'release_notes': ('版本说明', 'zh/mindstudio/830/releasenote/firstpage_0005_001.html', None),
    }

    p0_keys = ['operator_tools', 'profiling_tools', 'accuracy_tools']
    p1_keys = ['quickstart', 'llm_cases']
    p2_keys = ['msleaks', 'migration_tools', 'mstx_api']
    p3_keys = ['release_notes']

    # Determine which sections to crawl
    if args.section and args.section != 'all':
        if args.section not in all_sections:
            print(f"Unknown section: {args.section}")
            print(f"Available: {', '.join(all_sections.keys())}")
            sys.exit(1)
        sections_to_crawl = [args.section]
    elif args.section == 'all':
        sections_to_crawl = p0_keys + p1_keys + p2_keys + p3_keys
    else:
        sections_to_crawl = p0_keys

    for section_key in sections_to_crawl:
        display_name, start_path, plan_keys = all_sections[section_key]

        # Merge plan data from multiple keys if needed
        merged_pages = None
        if plan_keys:
            merged_pages = []
            for pk in plan_keys:
                if pk in crawl_plan_data:
                    merged_pages.extend(crawl_plan_data[pk])
        else:
            merged_pages = crawl_plan_data.get(display_name)

        crawl_section(section_key, start_path, corpus_base, merged_pages)


if __name__ == "__main__":
    main()
