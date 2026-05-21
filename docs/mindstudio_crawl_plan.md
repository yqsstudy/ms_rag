# MindStudio 全生态文档爬取计划

> 目标: 将 hiascend.com 上 MindStudio 全生态文档爬取为 RAG 语料
> 入口: https://www.hiascend.com/document/detail/zh/mindstudio/830/index/index.html
> 总计: 16 个板块, 724+ 页

---

## 一、板块总览与优先级

### P0 - 核心工具链 (最高优先级)

| # | 板块 | 页数 | 语料目录 | 状态 | 说明 |
|---|------|------|----------|------|------|
| 1 | 算子开发工具 | 183 | `corpus/operator_tools` | ✅ 已完成 | msKPP/msOpGen/msOpST/msSanitizer/msDebug/msProf, 183页→879 chunks |
| 2 | 性能调优工具 | 254 | `corpus/profiling_tools` | ✅ 已完成 | msprof采集/解析/可视化, MSPTI, 服务化调优, 254页→1090 chunks |
| 3 | 精度调试工具 | 57 | `corpus/accuracy_tools` | ✅ 已完成 | 精度比对/溢出分析/dump数据处理, 57页→176 chunks |

**优先理由**: 这三个板块构成昇腾开发的核心工具链 — 算子开发 → 性能调优 → 精度调试, 页数最多, 内容最密集, 是开发者最常查阅的文档。

### P1 - 实践案例与入门 (高优先级)

| # | 板块 | 页数 | 语料目录 | 状态 | 说明 |
|---|------|------|----------|------|------|
| 4 | 快速入门 | 37 | `corpus/quickstart` | ✅ 已完成 | 训练/推理/算子三大场景快速上手, 37页→189 chunks |
| 5 | 大模型训练精度问题定位案例 | 16 | `corpus/llm_cases` | ✅ 已完成 | 精度问题分场景定位, 含硬件压测案例 |
| 6 | 大模型推理精度问题分析案例 | 8 | `corpus/llm_cases` | ✅ 已完成 | logits采集比对, 算子精度预检 |
| 7 | 大模型训练性能瓶颈定位流程案例 | 7 | `corpus/llm_cases` | ✅ 已完成 | Ascend PyTorch Profiler + Insight定位 |
| 8 | 大模型推理量化调试调优指南 | 3 | `corpus/llm_cases` | ✅ 已完成 | 量化精度调优 |
| 9 | 传统模型推理迁移调试调优全流程指南 | 7 | `corpus/llm_cases` | ✅ 已完成 | 迁移调试+性能调优案例 |
| 10 | 内存问题分析案例 | 4 | `corpus/llm_cases` | ✅ 已完成 | 内存调优案例 |

**优先理由**: 大模型相关案例是当前热点, 实践案例对RAG问答价值极高。多个小板块合并为一个语料目录。

### P2 - 辅助工具与参考 (中优先级)

| # | 板块 | 页数 | 语料目录 | 状态 | 说明 |
|---|------|------|----------|------|------|
| 11 | msLeaks内存泄漏检测工具 | 18 | `corpus/msleaks` | ✅ 已完成 | 内存泄漏检测, Python/命令行/mstx采集, 18页→80 chunks |
| 12 | 分析迁移工具 | 14 | `corpus/migration_tools` | ✅ 已完成 | GPU→NPU迁移分析, 14页→44 chunks |
| 13 | mstx API参考 | 14 | `corpus/mstx_api` | ✅ 已完成 | 打点API接口文档, 14页→92 chunks |

### P3 - 版本与元信息 (低优先级)

| # | 板块 | 页数 | 语料目录 | 状态 | 说明 |
|---|------|------|----------|------|------|
| 14 | 版本说明 | 5 | `corpus/release_notes` | ✅ 已完成 | 版本配套/变更/漏洞修补, 5页→9 chunks |

### 已有语料

| # | 板块 | 页数 | 语料目录 | 状态 | 说明 |
|---|------|------|----------|------|------|
| - | MindStudio Insight工具 | 71 | `corpus/msinsight` | ✅ 已完成 | 含38个md文件, 541张图片 |
| - | 性能问题通用定位指南 | 80 | `corpus/performance_guide` | ✅ 已完成 | 含41个md文件, 115张图片 |

---

## 二、爬取技术方案

### 2.1 内容获取API

```
原始HTML文档: https://www.hiascend.com/doc_center/source/{page_path}
页面导航API:  https://www.hiascend.com/ascendgateway/ascendservice/doc/page/breadcrumbs/{page_path_90x}
```

- `page_path` 示例: `zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_001.html`
- breadcrumbs API 中 `.html` 需替换为 `_90x_html`
- 需携带 `Referer` 和 `User-Agent` 请求头

### 2.2 页面遍历策略

每个板块通过 breadcrumbs API 的 `nextNodeUrl` 字段链式遍历:
1. 从板块首页开始
2. 获取 breadcrumbs 中的 `nextNodeUrl`
3. 重复直到无 next 或回到上级

### 2.3 内容转换流程

```
HTML → 解析 → 提取正文 → 转Markdown → 添加frontmatter → 下载图片 → 更新图片路径
```

**HTML解析要点**:
- 使用 BeautifulSoup 解析 `/doc_center/source/` 返回的HTML
- 提取 `<h1>` ~ `<h4>` 作为标题, `<p>`, `<table>`, `<code>`, `<ul>/<ol>` 作为正文
- 图片路径需拼接 `https://www.hiascend.com/doc_center/source/` 前缀
- 过滤导航元素、面包屑、页脚等非正文内容

### 2.4 输出格式

每个页面生成一个 `.md` 文件, 格式与现有语料一致:

```yaml
---
title: "页面标题"
source: "https://www.hiascend.com/document/detail/{page_path}"
date_collected: "2026-05-04"
category: "板块名称"
original_path: "{page_path}"
---

# 页面标题

正文内容...
```

图片统一放入 `images/` 子目录, 引用路径为 `images/xxx.png`。

---

## 三、爬取批次规划

### 第一批 (P0 核心工具链)

| 批次 | 板块 | 预计页数 | 预计时间 | 备注 |
|------|------|----------|----------|------|
| 1a | 算子开发工具 | 183 | ~30min | 含大量API文档, 单页内容较长 |
| 1b | 性能调优工具 | 200+ | ~35min | 可能超过200页, 需确认上限 |
| 1c | 精度调试工具 | 57 | ~10min | |

### 第二批 (P1 实践案例)

| 批次 | 板块 | 预计页数 | 预计时间 | 备注 |
|------|------|----------|----------|------|
| 2a | 快速入门 | 37 | ~8min | |
| 2b | 大模型相关案例 (合并) | 45 | ~10min | 6个小板块合并为一个语料目录 |

### 第三批 (P2 辅助工具)

| 批次 | 板块 | 预计页数 | 预计时间 | 备注 |
|------|------|----------|----------|------|
| 3a | msLeaks + 分析迁移 + mstx API | 46 | ~10min | 3个小板块 |
| 3b | 版本说明 | 5 | ~2min | |

---

## 四、进度追踪

### 第一批: P0 核心工具链

- [x] **1a 算子开发工具** (183页) → `corpus/operator_tools`
  - [x] 页面列表枚举
  - [x] HTML内容爬取
  - [x] Markdown转换
  - [x] build_index.py 验证 (183页→879 chunks)

- [x] **1b 性能调优工具** (254页) → `corpus/profiling_tools`
  - [x] 页面列表枚举 (实际254页, 超出预期)
  - [x] HTML内容爬取
  - [x] Markdown转换
  - [x] build_index.py 验证 (254页→1090 chunks)

- [x] **1c 精度调试工具** (57页) → `corpus/accuracy_tools`
  - [x] 页面列表枚举
  - [x] HTML内容爬取
  - [x] Markdown转换
  - [x] build_index.py 验证 (57页→176 chunks)

### 第二批: P1 实践案例

- [x] **2a 快速入门** (37页) → `corpus/quickstart`
  - [x] 页面列表枚举
  - [x] HTML内容爬取
  - [x] Markdown转换
  - [x] build_index.py 验证 (37页→189 chunks)

- [x] **2b 大模型相关案例** (80页) → `corpus/llm_cases`
  - [x] 页面列表枚举 (实际80页, 超出预期45页)
  - [x] HTML内容爬取
  - [x] Markdown转换
  - [x] build_index.py 验证 (80页→186 chunks)

### 第三批: P2 辅助工具

- [x] **3a msLeaks** (18页) → `corpus/msleaks`
  - [x] HTML内容爬取 (18页→80 chunks)

- [x] **3b 分析迁移工具** (14页) → `corpus/migration_tools`
  - [x] HTML内容爬取 (14页→44 chunks)

- [x] **3c mstx API参考** (14页) → `corpus/mstx_api`
  - [x] HTML内容爬取 (14页→92 chunks)

### 第四批: P3 版本说明

- [x] **4a 版本说明** (5页) → `corpus/release_notes`
  - [x] HTML内容爬取 (5页→9 chunks)

---

## 五、质量检查清单

每个板块爬取完成后需验证:

- [ ] 所有页面均已爬取, 无遗漏
- [ ] Markdown格式正确, 标题层级清晰
- [ ] 图片全部下载且路径正确
- [ ] YAML frontmatter 完整 (title, source, date_collected, category)
- [ ] `build_index.py --corpus` 可正常处理
- [ ] chunk数量合理 (参考: 71页Insight → 780 chunks)
- [ ] 无乱码、无HTML标签残留

---

## 六、最终语料库全景 (目标)

| 语料目录 | 板块 | 页数 | 状态 |
|----------|------|------|------|
| `corpus/performance_guide` | 性能问题通用定位指南 | 80 | ✅ |
| `corpus/msinsight` | MindStudio Insight工具 | 71 | ✅ |
| `corpus/operator_tools` | 算子开发工具 | 183 | ✅ |
| `corpus/profiling_tools` | 性能调优工具 | 254 | ✅ |
| `corpus/accuracy_tools` | 精度调试工具 | 57 | ✅ |
| `corpus/quickstart` | 快速入门 | 37 | ✅ |
| `corpus/llm_cases` | 大模型相关案例 | 80 | ✅ |
| `corpus/msleaks` | msLeaks内存泄漏检测 | 18 | ✅ |
| `corpus/migration_tools` | 分析迁移工具 | 14 | ✅ |
| `corpus/mstx_api` | mstx API参考 | 14 | ✅ |
| `corpus/release_notes` | 版本说明 | 5 | ✅ |
| **总计** | | **803+** | |
