---
title: "使用步骤"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_012.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_012.html"
---

# 使用步骤

模型调优可以分为性能采集和性能分析两个步骤，具体介绍如下：

1. **采集性能日志：**[建议先分析Profiling日志，工具使用方法请参见模型调优性能采集工具](toolsample6_013.html)。
  - 首次采集性能数据时，建议仅采集L1、不开启堆栈（即with_stack为False），可以设置warmup为1，并设置active为2，采集两个step的数据。
  - 若涉及竞品分析，建议在相同条件下（包括但不限于采集的step数、超参数设置以及使用数据等）同步收集竞品的性能指标。

2. **分析性能瓶颈：**收集到Profiling日志后，可使用性能分析工具进行瓶颈分析。
  1. [使用msprof-analyze工具初步分析，粗粒度定位性能问题，并为后续的深入分析提供明确的方向，具体请参见模型调优快速分析（msprof-analyze命令行工具）](toolsample6_014.html)。
  2. [通过MindStudio Insight工具进一步识别瓶颈点，深入剖析问题根源。具体请参见模型调优深入分析（MindStudio Insight）](toolsample6_015.html)。

**父主题：**[模型调优工具](toolsample6_011.html)