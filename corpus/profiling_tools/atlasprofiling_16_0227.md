---
title: "MstxMonitor.enable_domain"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0227.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0227.html"
---

# MstxMonitor.enable_domain

函数

**def enable_domain(self, domain_name: str):**

函数功能

开启对应域打点的采集。

输入说明

domain_name：对应打点域的名称。

可以通过多次调用接口来开启多个域的采集。默认所有域的采集均已开启。

返回值说明

返回MsptiResult.MSPTI_SUCCESS表示成功，domain_name为空字符串时返回MsptiResult.MSPTI_ERROR_INVALID_PARAMETER，表示失败。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[MstxMonitor](atlasprofiling_16_0224.html)