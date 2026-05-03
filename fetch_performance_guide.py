#!/usr/bin/env python3
"""
性能定位指南文档爬虫
从昇腾社区网站获取性能定位指南的所有实践案例内容
"""

import os
import re
import requests
from bs4 import BeautifulSoup
import html2text
import urllib.parse
from pathlib import Path

# 基础URL
BASE_URL = "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue"

# 实践案例页面列表
PAGES = [
    {"file": "toolsample6_001.html", "title": "文档简介"},
    {"file": "toolsample6_002.html", "title": "概述"},
    {"file": "toolsample6_003.html", "title": "性能问题的定位流程"},
    {"file": "toolsample6_005.html", "title": "问题信息收集"},
    {"file": "toolsample6_006.html", "title": "排查思路介绍"},
    {"file": "toolsample6_008.html", "title": "性能问题排查"},
    {"file": "toolsample6_009.html", "title": "性能工具的使用"},
    {"file": "toolsample6_011.html", "title": "性能工具介绍"},
    {"file": "toolsample6_013.html", "title": "模型调优性能采集工具"},
    {"file": "toolsample6_014.html", "title": "模型调优快速分析"},
    {"file": "toolsample6_015.html", "title": "模型调优深入分析"},
    {"file": "toolsample6_018.html", "title": "集群性能分析"},
    {"file": "toolsample6_019.html", "title": "通信问题"},
    {"file": "toolsample6_020.html", "title": "算子性能问题"},
    {"file": "toolsample6_021.html", "title": "算子性能问题案例"},
    {"file": "toolsample6_022.html", "title": "下发异常问题"},
    {"file": "toolsample6_023.html", "title": "集群性能问题"},
    {"file": "toolsample6_024.html", "title": "Atlas 200I/500 A2推理产品场景"},
    {"file": "toolsample6_025.html", "title": "服务化工具"},
    {"file": "toolsample6_026.html", "title": "TopN性能问题的解决方案"},
    {"file": "toolsample6_028.html", "title": "MindIE推理场景"},
    {"file": "toolsample6_030.html", "title": "MindIE推理调优"},
    {"file": "toolsample6_032.html", "title": "MindIE服务化调优"},
    {"file": "toolsample6_034.html", "title": "版本升级"},
    {"file": "toolsample6_035.html", "title": "版本升级案例"},
    {"file": "toolsample6_036.html", "title": "版本升级实践"},
    {"file": "toolsample6_039.html", "title": "通信优化案例"},
    {"file": "toolsample6_042.html", "title": "性能优化实践"},
    {"file": "toolsample6_044.html", "title": "算子优化案例"},
    {"file": "toolsample6_046.html", "title": "下发优化案例"},
    {"file": "toolsample6_047.html", "title": "集群优化案例"},
    {"file": "toolsample6_048.html", "title": "推理优化案例"},
    {"file": "toolsample6_050.html", "title": "服务化优化案例"},
    {"file": "toolsample6_051.html", "title": "服务化调优案例"},
    {"file": "toolsample6_052.html", "title": "性能问题案例"},
    {"file": "toolsample6_054.html", "title": "性能分析案例"},
    {"file": "toolsample6_058.html", "title": "调优实践案例"},
    {"file": "toolsample6_062.html", "title": "性能诊断案例"},
    {"file": "toolsample6_075.html", "title": "高级调优案例"},
    {"file": "toolsample6_111.html", "title": "性能优化案例"},
    {"file": "toolsample6_116.html", "title": "其他案例"},
]

# 输出目录
OUTPUT_DIR = Path("/Users/ye/yangqisheng/ms_rag/corpus/performance_guide")

# 图片下载目录
IMAGES_DIR = OUTPUT_DIR / "images"

def setup_directories():
    """创建必要的目录"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def get_page_content(url):
    """获取页面HTML内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": BASE_URL
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"获取页面失败: {url}, 错误: {e}")
        return None

def clean_html_content(html_content):
    """清理HTML内容，移除JSON数据等"""
    # 移除 </html> 之后的所有内容
    end_tag = '</html>'
    if end_tag in html_content:
        idx = html_content.find(end_tag)
        html_content = html_content[:idx + len(end_tag)]
    return html_content

def extract_content_from_html(html_content):
    """从HTML中提取主要内容"""
    # 查找NUXT数据
    match = re.search(r'<script type="application/json" id="__NUXT_DATA__"[^>]*>(.*?)</script>', html_content, re.DOTALL)
    if match:
        data = match.group(1)
        # 在JSON数据中查找HTML内容
        parts = data.split('","')
        for part in parts:
            if '<!DOCTYPE html' in part or '<!doctype html' in part or 'topictitle' in part:
                # 提取HTML内容
                # 找到HTML开始位置（支持大小写）
                start_idx = part.find('<!DOCTYPE html')
                if start_idx == -1:
                    start_idx = part.find('<!doctype html')
                if start_idx == -1:
                    start_idx = part.find('\\u003C!DOCTYPE html')
                if start_idx == -1:
                    start_idx = part.find('\\u003C!doctype html')

                if start_idx != -1:
                    html_content_raw = part[start_idx:]
                    # 去掉末尾的引号和其他字符
                    end_idx = html_content_raw.rfind('</html>')
                    if end_idx != -1:
                        html_content_raw = html_content_raw[:end_idx + 7]

                    # 解码转义字符
                    html_content_raw = html_content_raw.replace('\\u003C', '<')
                    html_content_raw = html_content_raw.replace('\\u003E', '>')
                    html_content_raw = html_content_raw.replace('\\u0022', '"')
                    html_content_raw = html_content_raw.replace('\\n', '\n')
                    html_content_raw = html_content_raw.replace('\\t', '\t')
                    html_content_raw = html_content_raw.replace('\\/', '/')
                    html_content_raw = html_content_raw.replace('\\"', '"')

                    # 清理内容
                    html_content_raw = clean_html_content(html_content_raw)

                    return html_content_raw

    return None

def download_image(img_url, local_path):
    """下载图片到本地"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36",
        "Referer": BASE_URL
    }

    try:
        # 处理相对URL
        if not img_url.startswith('http'):
            img_url = urllib.parse.urljoin(BASE_URL, img_url)

        response = requests.get(img_url, headers=headers, timeout=30)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            f.write(response.content)

        print(f"  下载图片: {os.path.basename(local_path)}")
        return True
    except requests.RequestException as e:
        print(f"  下载图片失败: {img_url}, 错误: {e}")
        return False

def process_images(html_content, page_name):
    """处理HTML中的图片，下载并替换链接"""
    soup = BeautifulSoup(html_content, 'html.parser')

    images = soup.find_all('img')
    img_map = {}

    for idx, img in enumerate(images):
        src = img.get('src', '')
        if not src:
            continue

        # 生成本地文件名
        img_filename = os.path.basename(src.split('?')[0])
        if not img_filename or img_filename == '':
            img_filename = f"image_{idx}.png"

        # 清理文件名
        img_filename = re.sub(r'[^\w\-.]', '_', img_filename)

        # 添加页面前缀避免冲突
        local_filename = f"{page_name}_{img_filename}"
        local_path = IMAGES_DIR / local_filename

        # 下载图片
        if download_image(src, local_path):
            img_map[src] = local_filename
            # 更新HTML中的src
            img['src'] = f"images/{local_filename}"

    # 处理链接 - 保持相对链接并转换为绝对链接
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href and not href.startswith('http') and not href.startswith('#'):
            # 转换为绝对URL
            if href.endswith('.html'):
                a['href'] = f"{BASE_URL}/{href}?framework=pytorch"

    return str(soup), img_map

def html_to_markdown(html_content):
    """将HTML转换为Markdown"""
    h2t = html2text.HTML2Text()
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.ignore_emphasis = False
    h2t.body_width = 0  # 不自动换行
    h2t.skip_internal_links = False

    markdown = h2t.handle(html_content)
    return markdown

def save_markdown(markdown_content, filename, title, source_url):
    """保存Markdown文件"""
    filepath = OUTPUT_DIR / filename

    # 添加元信息
    header = f"""---
title: {title}
source: {source_url}
date_collected: 2026-04-29
---

# {title}

> 来源: [{source_url}]({source_url})

"""

    full_content = header + markdown_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"  保存文件: {filepath}")

def fetch_all_pages():
    """获取所有页面"""
    setup_directories()

    print("=" * 60)
    print("性能定位指南文档爬虫")
    print("=" * 60)

    for page_info in PAGES:
        url = f"{BASE_URL}/{page_info['file']}?framework=pytorch"
        print(f"\n[{page_info['title']}]")
        print(f"  URL: {url}")

        html_content = get_page_content(url)
        if not html_content:
            print(f"  跳过: 无法获取页面")
            continue

        # 提取主要内容
        content_html = extract_content_from_html(html_content)
        if not content_html:
            print(f"  跳过: 无法提取内容")
            continue

        # 处理图片
        page_name = page_info['file'].replace('.html', '')
        processed_html, img_map = process_images(content_html, page_name)

        # 转换为Markdown
        markdown = html_to_markdown(processed_html)

        # 保存文件
        md_filename = f"{page_name}.md"
        save_markdown(markdown, md_filename, page_info['title'], url)

        print(f"  完成: 下载了 {len(img_map)} 张图片")

    print("\n" + "=" * 60)
    print(f"完成！所有文档已保存到: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    fetch_all_pages()