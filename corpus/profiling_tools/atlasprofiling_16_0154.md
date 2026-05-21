---
title: "ai_vector_core_utilization（AI Vector Core指令占比）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0154.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0154.html"
---

# ai_vector_core_utilization（AI Vector Core指令占比）

AI Vector Core指令占比数据无timeline信息，summary信息在ai_vector_core_utilization_*.csv文件汇总。

#### 支持的型号

Atlas 200I/500 A2 推理产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

#### ai_vector_core_utilization_*.csv文件说明

ai_vector_core_utilization_*.csv文件内容格式示例如下：
**图1**
ai_vector_core_utilization_*.csv**表1**字段说明
字段名

字段含义

vec_ratio

代表vec类型指令（向量类运算指令）的cycle数在total cycle数中的占用比。Atlas 200I/500 A2 推理产品不支持该字段，给予默认值N/A。

mac_ratio

代表cube类型指令（fp16及s16矩阵类运算指令）的cycle数在total cycle数中的占用比。

scalar_ratio

代表scalar类型指令（标量类运算指令）的cycle数在total cycle数中的占用比。

mte1_ratio

代表mte1类型指令（L1->L0A/L0B搬运类指令）的cycle数在total cycle数中的占用比。

mte2_ratio

代表mte2类型指令（DDR->AICORE搬运类指令）的cycle数在total cycle数中的占用比。（Atlas 200I/500 A2 推理产品）

mte2_ratio

代表mte2类型指令（片上内存->AICORE搬运类指令）的cycle数在total cycle数中的占用比。（Atlas A2 训练系列产品/Atlas A2 推理系列产品）（Atlas A3 训练系列产品/Atlas A3 推理系列产品）

mte3_ratio

代表mte3类型指令（AICORE->DDR搬运类指令）的cycle数在total cycle数中的占用比。（Atlas 200I/500 A2 推理产品）

mte3_ratio

代表mte3类型指令（AICORE->片上内存搬运类指令）的cycle数在total cycle数中的占用比。（Atlas A2 训练系列产品/Atlas A2 推理系列产品）（Atlas A3 训练系列产品/Atlas A3 推理系列产品）

icache_miss_rate

代表icache缺失率，即未命中instruction的L1 cache，数值越小越好。

memory_bound

用于识别AICore执行算子计算过程是否存在Memory瓶颈，由mte2_ratio/max(mac_ratio, vec_ratio)计算得出。计算结果小于1，表示没有Memory瓶颈；计算结果大于1则表示有Memory瓶颈，且数值越大瓶颈越严重。

[此处AI Vector Core性能指标采集项以sample-based场景的PipeUtilization为例，更多参数解析参见ai_core_utilization（AI Core指令占比）](atlasprofiling_16_0153.html#ZH-CN_TOPIC_0000002504198586)。
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
**父主题：**[性能数据文件参考](atlasprofiling_16_0140.html)