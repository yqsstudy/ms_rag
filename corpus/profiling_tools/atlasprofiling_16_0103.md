---
title: "__enter__/__exit__"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0103.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0103.html"
---

# __enter__/__exit__

函数

def __enter__(self)

def __exit__(self, exc_type, exc_val, exc_tb)

函数功能

在进入的时候，自动调用span_start函数，用于记录过程开始的时间点；在退出的时候，自动调用span_end函数，用于记录过程的结束时间点。
|  |  |
| --- | --- |
|  |  |
**父主题：**[服务化调优](atlasprofiling_16_0100.html)