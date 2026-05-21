---
title: "biu_group/aic_core_group/aiv_core_group（AI Core和AI Vector的带宽和延时）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0174.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0174.html"
---

# biu_group/aic_core_group/aiv_core_group（AI Core和AI Vector的带宽和延时）

AI Core和AI Vector的带宽和延时数据无summary信息，timeline信息在msprof_*.json文件的biu_group、aic_core_group、aiv_core_group层级展示。

#### 支持的型号

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

#### msprof_*.json文件的biu_group、aic_core_group、aiv_core_group层级数据说明
**图1**
**biu_group
图2**
**aic_core_group
图3**
aiv_core_group**表1**字段说明
字段名

字段含义

**biu_group**

Bandwidth Read

BIU总线接口单元读取指令时的带宽。

Bandwidth Write

BIU总线接口单元写入指令时的带宽。

Latency Read

BIU总线接口单元读取指令时的时延。

Latency Write

BIU总线接口单元写入指令时的时延。

**aic_core_group**

Cube

矩阵类运算指令在本采样周期内的cycle数和占比。

Mte1

L1->L0A/L0B搬运类指令在本采样周期内的cycle数和占比。

Mte2

片上内存->AICORE搬运类指令在本采样周期内的cycle数和占比。

Mte3

AICORE->片上内存搬运类指令在本采样周期内的cycle数和占比。

**aiv_core_group**

Mte1

L1->L0A/L0B搬运类指令在本采样周期内的cycle数和占比。

Mte2

片上内存->AICORE搬运类指令在本采样周期内的cycle数和占比。

Mte3

AICORE->片上内存搬运类指令在本采样周期内的cycle数和占比。

Scalar

标量类运算指令在本采样周期内的cycle数和占比。

Vector

向量类运算指令在本采样周期内的cycle数和占比。
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
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[性能数据文件参考](atlasprofiling_16_0140.html)