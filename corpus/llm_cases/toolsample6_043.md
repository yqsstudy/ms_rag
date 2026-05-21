---
title: "案例：ZeRO3模式导致通信小包"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_043.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_043.html"
---

# 案例：ZeRO3模式导致通信小包

#### 问题描述

同一模型从NPU迁移至GPU，性能不达标。

#### 问题分析

[使用模型调优快速分析（msprof-analyze命令行工具）](toolsample6_014.html)中的compare性能比对工具，对比基线GPU和迁移后的NPU的数据，发现通信未掩盖时间存在较大差距，如图1所示。
**图1**
compare对比GPU与NPU
对比基线GPU与迁移后NPU的时间线（Timeline），发现差异主要来源于Step结尾的allGather通信部分，NPU耗时100ms左右，GPU耗时仅4ms左右，如图2所示。
**图2**
GPU与NPU的Timeline对比
NPU这部分通信算子带宽仅0.2GB/s，观察到存在大量allGather通信算子，传输数据量仅256byte，通信建链占据大部分耗时，如图3所示。这部分算子主要在进行ZeRO3操作。
**图3**
allGather通信小包算子
ZeRO（Zero Redundancy Optimizer，零冗余优化器）模式是一种节省内存的方法，ZeRO模式会带来通信策略的变化。ZeRO的主要原理是将优化器状态、梯度、权重等数据进行切分，在需要使用时再通过集合通信进行同步，来减少显存的使用峰值，是一种典型的时间换空间的办法。

#### 问题解决

将ZeRO3算法修改为ZeRO2算法，即不再对模型权重进行切分，虽然会增加显存占用，但是减少了设备间的通信开销。替换为ZeRO2后，总体性能提升2.7%。
**父主题：**[通信小包](toolsample6_042.html)