#!/usr/bin/env python3
"""
性能定位指南文档爬虫 - 修复版
正确处理图片下载
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
DOC_SOURCE_URL = "https://www.hiascend.com/doc_center/source/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue"

# 输出目录
OUTPUT_DIR = Path("/Users/ye/yangqisheng/ms_rag/corpus/performance_guide")
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
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"获取页面失败: {url}, 错误: {e}")
        return None

def clean_html_content(html_content):
    """清理HTML内容，移除JSON数据等"""
    end_tag = '</html>'
    if end_tag in html_content:
        idx = html_content.find(end_tag)
        html_content = html_content[:idx + len(end_tag)]
    return html_content

def extract_content_from_html(html_content):
    """从HTML中提取主要内容"""
    match = re.search(r'<script type="application/json" id="__NUXT_DATA__"[^>]*>(.*?)</script>', html_content, re.DOTALL)
    if match:
        data = match.group(1)
        parts = data.split('","')
        for part in parts:
            if '<!DOCTYPE html' in part or '<!doctype html' in part or 'topictitle' in part:
                start_idx = part.find('<!DOCTYPE html')
                if start_idx == -1:
                    start_idx = part.find('<!doctype html')
                if start_idx == -1:
                    start_idx = part.find('\\u003C!DOCTYPE html')
                if start_idx == -1:
                    start_idx = part.find('\\u003C!doctype html')

                if start_idx != -1:
                    html_content_raw = part[start_idx:]
                    end_idx = html_content_raw.rfind('</html>')
                    if end_idx != -1:
                        html_content_raw = html_content_raw[:end_idx + 7]

                    html_content_raw = html_content_raw.replace('\\u003C', '<')
                    html_content_raw = html_content_raw.replace('\\u003E', '>')
                    html_content_raw = html_content_raw.replace('\\u0022', '"')
                    html_content_raw = html_content_raw.replace('\\n', '\n')
                    html_content_raw = html_content_raw.replace('\\t', '\t')
                    html_content_raw = html_content_raw.replace('\\/', '/')
                    html_content_raw = html_content_raw.replace('\\"', '"')
                    html_content_raw = clean_html_content(html_content_raw)
                    return html_content_raw
    return None

def download_image(img_src, local_path, page_file):
    """下载图片到本地"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": BASE_URL
    }

    try:
        # 构建正确的图片URL
        # 图片路径是相对于文档源文件的
        # 例如: public_sys-resources/note_3.0-zh-cn.png
        # 完整URL: https://www.hiascend.com/doc_center/source/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/public_sys-resources/note_3.0-zh-cn.png

        if img_src.startswith('http'):
            img_url = img_src
        else:
            # 使用文档源URL作为基础
            img_url = f"{DOC_SOURCE_URL}/{img_src}"

        response = requests.get(img_url, headers=headers, timeout=30)
        response.raise_for_status()

        # 检查是否真的是图片
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print(f"  跳过非图片内容: {img_src} (content-type: {content_type})")
            return False

        with open(local_path, 'wb') as f:
            f.write(response.content)

        print(f"  下载图片: {os.path.basename(local_path)}")
        return True
    except requests.RequestException as e:
        print(f"  下载图片失败: {img_src}, 错误: {e}")
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
        if download_image(src, local_path, page_name):
            img_map[src] = local_filename
            # 更新HTML中的src
            img['src'] = f"images/{local_filename}"
        else:
            # 下载失败，保留原始URL
            img['src'] = f"{DOC_SOURCE_URL}/{src}"

    # 处理链接 - 保持相对链接并转换为绝对链接
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href and not href.startswith('http') and not href.startswith('#'):
            if href.endswith('.html'):
                a['href'] = f"{BASE_URL}/{href}?framework=pytorch"

    return str(soup), img_map

def html_to_markdown(html_content):
    """将HTML转换为Markdown"""
    h2t = html2text.HTML2Text()
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.ignore_emphasis = False
    h2t.body_width = 0
    h2t.skip_internal_links = False
    return h2t.handle(html_content)

def save_markdown(markdown_content, filename, title, source_url):
    """保存Markdown文件"""
    filepath = OUTPUT_DIR / filename
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

def fetch_page(page_file, title):
    """获取单个页面"""
    url = f"{BASE_URL}/{page_file}?framework=pytorch"
    print(f"\n[{title}]")
    print(f"  URL: {url}")

    html_content = get_page_content(url)
    if not html_content:
        print(f"  跳过: 无法获取页面")
        return False

    content_html = extract_content_from_html(html_content)
    if not content_html:
        print(f"  跳过: 无法提取内容")
        return False

    page_name = page_file.replace('.html', '')
    processed_html, img_map = process_images(content_html, page_name)

    markdown = html_to_markdown(processed_html)

    md_filename = f"{page_name}.md"
    save_markdown(markdown, md_filename, title, url)

    print(f"  完成: 下载了 {len(img_map)} 张图片")
    return True

def get_all_page_links():
    """从已下载的文件中获取所有页面链接"""
    all_links = set()
    for md_file in OUTPUT_DIR.glob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        links = re.findall(r'toolsample6_\d+\.html', content)
        all_links.update(links)
    return sorted(all_links)

def main():
    """主函数"""
    setup_directories()

    # 获取所有已知的页面链接
    existing_pages = set()
    for md_file in OUTPUT_DIR.glob("*.md"):
        name = md_file.stem + ".html"
        existing_pages.add(name)

    # 获取所有链接
    all_links = get_all_page_links()

    # 找出缺失的页面
    missing_pages = [link for link in all_links if link not in existing_pages]

    if missing_pages:
        print(f"发现 {len(missing_pages)} 个缺失的页面需要重新获取")
        print(f"缺失页面: {missing_pages}")

        # 清理旧的无效图片文件
        print("\n清理无效图片文件...")
        for img_file in IMAGES_DIR.glob("*"):
            if img_file.is_file():
                # 检查是否是有效的图片文件
                with open(img_file, 'rb') as f:
                    header = f.read(10)
                    # PNG文件以 89 50 4E 47 开头
                    # JPEG文件以 FF D8 开头
                    # GIF文件以 47 49 46 开头
                    if not (header[:4] == b'\x89PNG' or header[:2] == b'\xff\xd8' or header[:3] == b'GIF'):
                        print(f"  删除无效文件: {img_file.name}")
                        img_file.unlink()

        # 重新获取所有页面（修复图片下载）
        print("\n重新获取所有页面以修复图片...")

        # 页面标题映射
        page_titles = {
            "toolsample6_001.html": "文档简介",
            "toolsample6_002.html": "概述",
            "toolsample6_003.html": "性能问题的定位流程",
            "toolsample6_005.html": "问题信息收集",
            "toolsample6_006.html": "排查思路介绍",
            "toolsample6_008.html": "性能问题排查",
            "toolsample6_009.html": "性能工具的使用",
            "toolsample6_011.html": "性能工具介绍",
            "toolsample6_013.html": "模型调优性能采集工具",
            "toolsample6_014.html": "模型调优快速分析",
            "toolsample6_015.html": "模型调优深入分析",
            "toolsample6_018.html": "集群性能分析",
            "toolsample6_019.html": "通信问题",
            "toolsample6_020.html": "算子性能问题",
            "toolsample6_021.html": "算子性能问题案例",
            "toolsample6_022.html": "下发异常问题",
            "toolsample6_023.html": "集群性能问题",
            "toolsample6_024.html": "Atlas 200I/500 A2推理产品场景",
            "toolsample6_025.html": "服务化工具",
            "toolsample6_026.html": "TopN性能问题的解决方案",
            "toolsample6_028.html": "MindIE推理场景",
            "toolsample6_030.html": "MindIE推理调优",
            "toolsample6_032.html": "MindIE服务化调优",
            "toolsample6_034.html": "版本升级",
            "toolsample6_035.html": "版本升级案例",
            "toolsample6_036.html": "版本升级实践",
            "toolsample6_039.html": "通信优化案例",
            "toolsample6_042.html": "性能优化实践",
            "toolsample6_044.html": "算子优化案例",
            "toolsample6_046.html": "下发优化案例",
            "toolsample6_047.html": "集群优化案例",
            "toolsample6_048.html": "推理优化案例",
            "toolsample6_050.html": "服务化优化案例",
            "toolsample6_051.html": "服务化调优案例",
            "toolsample6_052.html": "性能问题案例",
            "toolsample6_054.html": "性能分析案例",
            "toolsample6_058.html": "调优实践案例",
            "toolsample6_062.html": "性能诊断案例",
            "toolsample6_075.html": "高级调优案例",
            "toolsample6_111.html": "性能优化案例",
            "toolsample6_116.html": "其他案例",
        }

        for page_file in all_links:
            title = page_titles.get(page_file, page_file.replace('.html', ''))
            fetch_page(page_file, title)

    print("\n" + "=" * 60)
    print(f"完成！所有文档已保存到: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()