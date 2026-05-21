---
title: "内存劣化对比分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_120.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_120.html"
---

# 内存劣化对比分析

算子内存比对结果在performance_comparison_result_*.xlsx中“MemoryCompare”和“MemoryCompareStatistic”的sheet页呈现。

1. 查看“MemoryCompareStatistic”页，找出内存占用差距TOP的算子。
2. 查看“MemoryCompare”页，搜索内存占用差距TOP的算子，查看具体占用的算子。

例如：现场某次升级CANN软件包和PTA软件包后，发生OOM情况，于是采集升级前后两次的Profiling，根据算子级比对发现是aten::group_norm多申请了10GB+内存，如图1所示。
**图1**
算子比对

**父主题：**[版本升级性能劣化定位方法论](toolsample6_116.html)