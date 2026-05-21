---
title: "HcclMonitor.start"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0215.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0215.html"
---

# HcclMonitor.start

函数

**def start(self, cb: Callable[[HcclData], None]) -> MsptiResult:**

函数功能

标识通信算子性能数据采集的开始。

输入说明

[cb：回调函数，用于传递采集到的通信数据。调用结构体HcclData](atlasprofiling_16_0232.html#ZH-CN_TOPIC_0000002536158443)。

返回值说明

返回MsptiResult.MSPTI_SUCCESS表示成功，返回MsptiResult.MSPTI_ERROR_INVALID_PARAMETER，则回调函数类型不正确，表示失败。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[HcclMonitor](atlasprofiling_16_0214.html)