---
title: "工具介绍"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0021.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0021.html"
---

# 工具介绍

MSPTI调优工具（MSPTI，MindStudio Profiling Tool Interface）是MindStudio针对Ascend设备提出的一套Profiling API，用户可以通过MSPTI构建针对NPU应用程序的工具，用于分析应用程序的性能。

MSPTI为通用场景接口，使用MSPTI API开发的Profiling分析工具可以在各种框架的推理训练场景生效。

MSPTI主要包括以下功能：

- Tracing：在MSPTI中Tracing是指CANN应用程序执行启动CANN活动的时间戳和附加信息的收集，如CANN API、Kernel、内存拷贝等。通过了解程序运行耗时，识别CANN代码的性能问题。可以使用Activity API和Callback API收集Tracing信息。
- Profiling：在MSPTI中Profiling是指单独收集一个或一组Kernel的NPU性能指标。

MSPTI当前提供使用C开发的一套API以及将C API的功能作为底层逻辑封装的一套Python的API。

#### 约束

MSPTI工具不可与任何其他性能数据采集工具同时使用，否则会导致采集的数据丢失。

#### 支持的型号

Atlas 200I/500 A2 推理产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品
**父主题：**[MSPTI调优工具](atlasprofiling_16_0020.html)