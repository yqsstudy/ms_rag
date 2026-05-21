---
title: "ai_cpu_top_function（AI CPU热点函数）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0183.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0183.html"
---

# ai_cpu_top_function（AI CPU热点函数）

AI CPU热点函数数据无timeline信息，summary信息在ai_cpu_top_function_*.csv文件汇总。

#### 支持的型号

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

#### ai_cpu_top_function_*.csv文件说明

ai_cpu_top_function_*.csv文件内容格式示例如下：
**图1**
ai_cpu_top_function_*.csv**表1**字段说明
字段名

字段含义

Device_id

设备ID。

Function

AI CPU模块的热点函数。

Module

函数所在的模块名。

Cycles

统计时间内函数消耗的Cycle数。

Cycles(%)

统计时间内函数消耗的Cycle数对于统计时长的占比。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[性能数据文件参考](atlasprofiling_16_0140.html)