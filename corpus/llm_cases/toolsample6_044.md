---
title: "源地址与目的地址字节未对齐"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_044.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_044.html"
---

# 源地址与目的地址字节未对齐

字节未对齐，指的是在集群进行通信时，如果源地址或目的地址没有按照特定的字节对齐（例如512字节对齐），会导致传输带宽显著下降，进而影响通信性能。这种未对齐问题常见于SDMA传输（即节点内传输），多出现于ZeRO算法中。解决方法通常包括对数据进行适当的填充（padding），以确保地址对齐，从而优化通信性能。

#### 问题描述
单机八卡性能低于预期。通过MindStudio Insight的通信矩阵分析，发现平均带宽很低，只有1-2GB/s，远低于经验值，如图1所示。**图1**
集群通信矩阵分析
#### 问题分析
进一步定位具体算子，发现是一个allGather算子带宽特别低，耗时300+ms，带宽只有0.1GB/，如图2所示。**图2**
allGather算子Timeline选中详情
经HCCL专家分析，是DP通信域的allGather通信算子源地址与目标地址无法对齐，导致通信性能劣化严重。

#### 问题解决

针对DP通信域的allGather入桶做字节对齐的padding，对齐字节。当前AscendSpeed已适配针对DP通信域的allGather入桶做了字节对齐的padding，DeepSpeed和Megatron还未修改，需要去DeepSpeed源码里改nccl_start_alignment_factor，如图3所示，修改后，allgather耗时从350ms变成了50ms。
**图3**
**修改nccl_start_alignment_factor令字节对齐

父主题：**[通信问题优化方案](toolsample6_028.html)