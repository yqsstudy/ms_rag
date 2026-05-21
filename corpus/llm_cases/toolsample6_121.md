---
title: "空闲时间劣化对比分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_121.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_121.html"
---

# 空闲时间劣化对比分析

当计算时间和通信时间无明显变化，但Free时间明显增大时，可以借助performance_comparison_result_*.xlsx中“ApiCompare”页的比对结果，找到耗时差距TOP的API，结合MindStudio Insight界面的下发连线，确认是否有Host bound。
**图1**
**查看ApiCompare页

父主题：**[版本升级性能劣化定位方法论](toolsample6_116.html)