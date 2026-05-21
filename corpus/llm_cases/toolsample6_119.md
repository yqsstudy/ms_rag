---
title: "通信时间（未被掩盖的）劣化对比分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_119.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_119.html"
---

# 通信时间（未被掩盖的）劣化对比分析

1. 确认是否存在显著的通信算子性能劣化现象。

打开performance_comparison_result_.xlsx文件中的“CommunicationCompare”工作表，重点对比以下通信大算子的性能指标，如图1所示。

  - 算子类型（Broadcast、AllReduce等）
  - 耗时指标（平均耗时、最大/最小耗时）与调用频次统计
  - 关联的子任务信息（Reduce_Inline、Notify_Record、Notify_Wait、Memcpy等）
**图1**
对比通信大算子的性能指标

2. 在“OverallMetrics”工作表中，按通信域维度进行深入对比分析。

需重点关注同一通信域下transit_time，wait time指标的差异分析，如图2所示。
**图2**
关注重点指标差异

3. 如果通信性能分析没有劣化的通信算子，代表通信与计算的并行度较差，继续进行NPU的集群性能分析。
**父主题：**[版本升级性能劣化定位方法论](toolsample6_116.html)