---
title: "cpu_usage（AI CPU、Ctrl CPU利用率）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0166.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0166.html"
---

# cpu_usage（AI CPU、Ctrl CPU利用率）

AI CPU（执行AI CPU算子）、Ctrl CPU（执行Driver任务）利用率数据无timeline信息，summary信息在cpu_usage_*.csv文件汇总。

#### 支持的型号

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

#### cpu_usage_*.csv文件数据说明

cpu_usage_*.csv文件内容格式示例如下：
**图1**
cpu_usage_*.csv**表1**字段说明
字段名

字段含义

Device_id

设备ID。

Cpu Type

CPU类型，包含AI CPU和Ctrl CPU。

User(%)

用户态进程执行时长（多个AI CPU和Ctrl CPU的平均值）占比。

Sys(%)

内核态进程执行时长（多个AI CPU和Ctrl CPU的平均值）占比。

IoWait(%)

IO等待状态时长（多个AI CPU和Ctrl CPU的平均值）占比。

Irq(%)

硬件中断时长（多个AI CPU和Ctrl CPU的平均值）占比。

Soft(%)

软件中断时长（多个AI CPU和Ctrl CPU的平均值）占比。

Idle(%)

空闲状态时长（多个AI CPU和Ctrl CPU的平均值）占比。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[性能数据文件参考](atlasprofiling_16_0140.html)