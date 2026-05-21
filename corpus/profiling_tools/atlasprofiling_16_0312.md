---
title: "其他工具"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0312.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0312.html"
---

# 其他工具

Driver包中提供了其他工具，用于协助Profiling工具进行性能数据采集，用户无需直接使用，相关说明如下表所示。
**表1**其他工具说明
工具名称

存储相对路径

功能说明及使用场景

风险分析

保留原因

perf

/usr/bin/perf

采集AI CPU利用率、Ctrl CPU利用率、进程CPU占用率、进程内存占用和系统内存占用等AI处理器性能数据。

用户配置系统级Profiling采集开关时，Profiling会使能此工具采集AI处理器性能数据。

仅用于采集或分析固定的一些AI处理器性能数据。无法获取其他运行状态信息，实际风险小。

属于系统级Profiling采集能力的一部分。
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
**父主题：**[附录](atlasprofiling_16_0209.html)