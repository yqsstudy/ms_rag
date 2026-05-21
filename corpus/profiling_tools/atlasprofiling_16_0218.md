---
title: "HcclMonitor.set_buffer_size"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0218.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0218.html"
---

# HcclMonitor.set_buffer_size

函数

**def set_buffer_size(cls, size: int) -> MsptiResult:**

函数功能

在采集开始前设置Activity Buffer的大小，用来存放采集到的性能数据。

在采集过程中，动态修改Activity Buffer的大小是不生效的，直到本次采集结束，下次采集开始才会生效。

输入说明

size：Activity Buffer的大小，单位MB，默认8MB。

仅支持配置为正整数，配置为其他非法值则返回失败，采集使用默认的Activity Buffer大小。

返回值说明

返回MsptiResult.MSPTI_SUCCESS表示成功，返回MsptiResult.MSPTI_ERROR_INVALID_PARAMETER，则参数设置不正确，表示失败。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[HcclMonitor](atlasprofiling_16_0214.html)