---
title: "确认主要性能瓶颈"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_117.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_117.html"
---

# 确认主要性能瓶颈
使用msprof-analyze compare工具，查看打点信息，如图1所示。或查看performance_comparison_result_{timestamp}.xlsx的OverallMetrics页。**图1**
打印信息

需重点关注四个核心维度差异，找到差异最明显的维度进一步分析。
- Computing Time（计算时间）
- Uncovered Communication Time（未被计算掩盖的通信时间）
- Mem Usage（内存使用）
- Free Time（空闲时间）
**父主题：**[版本升级性能劣化定位方法论](toolsample6_116.html)