---
title: "PyTorch使用Profiler导致性能膨胀现象"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_1200.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_1200.html"
---

# PyTorch使用Profiler导致性能膨胀现象

#### 现象

模型训练过程中，存在Profiler开始的step和结束的step，相对其他step耗时增长。

#### 原因

Profiler启动采集前，schedule的active或warmup的Profiler初始化存在开销，会有一定性能膨胀。

Profiler采集后的自动解析场景下，解析阶段会有较大性能膨胀。

#### 处理

在开启Profiler采集性能数据情况下，若需要参考step耗时，则可排除Profiler启动和解析对应的step耗时，仅参考中间部分的step耗时。
**父主题：**[FAQ](atlasprofiling_16_0314.html)