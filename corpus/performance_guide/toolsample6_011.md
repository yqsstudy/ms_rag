---
title: 性能工具介绍
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_011.html?framework=pytorch
date_collected: 2026-04-29
---

# 性能工具介绍

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_011.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_011.html?framework=pytorch)

# 使用步骤

模型调优可以分为性能采集和性能分析两个步骤，具体介绍如下：

  1. **采集性能日志：** 建议先分析Profiling日志，工具使用方法请参见[模型调优性能采集工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_013.html?framework=pytorch)。

![](images/toolsample6_011_note_3.0-zh-cn.png)

     * 首次采集性能数据时，建议仅采集L1、不开启堆栈（即with_stack为False），可以设置warmup为1，并设置active为2，采集两个step的数据。
     * 若涉及竞品分析，建议在相同条件下（包括但不限于采集的step数、超参数设置以及使用数据等）同步收集竞品的性能指标。

  2. **分析性能瓶颈：** 收集到Profiling日志后，可使用性能分析工具进行瓶颈分析。
     1. 使用msprof-analyze工具初步分析，粗粒度定位性能问题，并为后续的深入分析提供明确的方向，具体请参见[模型调优快速分析（msprof-analyze命令行工具）](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_014.html?framework=pytorch)。
     2. 通过MindStudio Insight工具进一步识别瓶颈点，深入剖析问题根源。具体请参见[模型调优深入分析（MindStudio Insight）](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_015.html?framework=pytorch)。



**父主题：** [模型调优工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_011.html?framework=pytorch)
