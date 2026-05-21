---
title: "KernelMonitor.start"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0220.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0220.html"
---

# KernelMonitor.start

函数

**def start(self, cb: Callable[[KernelData], None]) -> MsptiResult:**

函数功能

标识Kernel性能数据采集的开始。

输入说明

[cb：回调函数，用于传递采集到的Kernel数据。调用结构体KernelData](atlasprofiling_16_0233.html#ZH-CN_TOPIC_0000002504198628)。

返回值说明

返回MsptiResult.MSPTI_SUCCESS表示成功，返回MsptiResult.MSPTI_ERROR_INVALID_PARAMETER，则回调函数类型不正确，表示失败。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[KernelMonitor](atlasprofiling_16_0219.html)