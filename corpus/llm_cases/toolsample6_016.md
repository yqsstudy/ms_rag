---
title: "总体介绍"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_016.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_016.html"
---

# 总体介绍

MindStudio Insight工具能够将全量Profiling数据进行可视化呈现，帮助用户进一步分析并确认问题。

使用MindStudio Insight工具分析问题的流程如图1所示。
**图1**
![](figure/zh-cn_image_0000002503927414.png "点击放大")使用MindStudio Insight工具分析流程图
1. 使用集群分析功能初步定界
  1. [先进入概览（Summary）界面，通过多卡计算、通信、调度比对，初步确认问题分类。具体定界过程，详见概览（Summary）](toolsample6_019.html)。
  2. [再进入通信（Communication）界面，按通信域拆解，进一步定位慢卡或慢链路问题；确认异常卡或异常链路后，可直接根据通信算子跳转至时间线（Timeline）具体定位，详见通信（Communication）](toolsample6_020.html)。
    - 卡数较少时，可直接导入原始性能数据，自动生成集群分析结果（由可视化工具调用msprof-analyze命令行工具）。
    - 卡数过多、全量性能数据过于笨重时，推荐您以命令行方式手动调用msprof-analyze工具，用MindStudio Insight打开cluster_analysis_output集群分析结果交付件，更加轻便快捷。

2. 初步定界后，选择所需卡，从单卡维度进一步分析
  - [时间线（Timeline）界面：将训练或推理过程中Host、Device上的运行详细情况平铺在时间轴上，直观呈现Host侧的API耗时以及Device侧的Task耗时，具体使用思路详见时间线（Timeline）](toolsample6_022.html)。
  - [内存（Memory）界面：以内存折线图呈现整体内存趋势，可以框选放大折线图中峰值区域，精准定位到内存消耗大的进程或算子，具体使用思路详见内存（Memory）](toolsample6_023.html)。
  - [算子（Operator）界面：计算算子和通信算子的耗时统计，可按类型、Shape统计，同时支持两卡间比对功能，可更直观的查看算子详情，具体使用思路详见算子（Operator）](toolsample6_024.html)。

**父主题：**[模型调优深入分析（MindStudio Insight）](toolsample6_015.html)