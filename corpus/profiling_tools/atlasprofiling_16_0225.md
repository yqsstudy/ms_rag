---
title: "MstxMonitor.start"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0225.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0225.html"
---

# MstxMonitor.start

函数

**def start(self, mark_cb : Callable[[MarkerData], None] = empty_callback, range_cb : Callable[[RangeMarkerData], None] = empty_callback) -> MsptiResult:**

函数功能

标识数据采集mstx打点的开始。

输入说明

[mark_cb：回调函数，用于传递采集到的mstx瞬时打点数据。调用结构体MarkerData](atlasprofiling_16_0234.html#ZH-CN_TOPIC_0000002504358464)。

[range_cb：回调函数，用于传递采集到的mstx range打点数据。调用结构体RangeMarkerData](atlasprofiling_16_0235.html#ZH-CN_TOPIC_0000002536038417)。

返回值说明

返回MsptiResult.MSPTI_SUCCESS表示成功，返回MsptiResult.MSPTI_ERROR_INVALID_PARAMETER，则回调函数类型不正确，表示失败。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[MstxMonitor](atlasprofiling_16_0224.html)