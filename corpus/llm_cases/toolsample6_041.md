---
title: "通信重传典型案例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_041.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_041.html"
---

# 通信重传典型案例

#### 问题描述

LLaMA3-70B模型从4机迁移至32机集群时，发生线性度劣化。

#### 问题分析
如图1[所示，利用模型调优快速分析（msprof-analyze命令行工具）](toolsample6_014.html)分别对正常4机集群与异常32机集群进行分析，对比两者结果发现，耗时差异主要在通信上，32机集群整体通信耗时更长。**图1**
cluster_step_trace_time.csv交付件，正常4机与异常32机对比

以0卡为例，对比正常集群与异常集群的0卡，发现问题出现在迭代末尾的allReduce和broadcast算子上，如图2所示。**图2**
异常集群0卡Timeline

根据通信算子选中详情的dst rank（目标卡，在notify wait通信事件中一般代表被等待的慢卡）不断跳转，发现是440卡拖累了同一tp通信域内的其它卡，如图3所示。**图3**
异常集群440卡Timeline

进入通信（Communication）页签，选择通信耗时分析，找到对应通信域。按等待时间（Wait Time）升序排列，找到该通信域内等待时间较短、传输时间较长的卡。如图4所示。**图4**
通信（Communication）页签 > 通信耗时分析

进一步查看传输时间较长卡的带宽分析，发现存在大量带宽极低的RDMA通信包，如图5所示。怀疑存在网络传输问题，需要排查网络配置。**图5**带宽分析


#### 问题解决

排查网络配置后发现，交换机和计算节点服务器之间的流量走在了无PFC拥塞控制的队列上，导致相应队列上网络出现大量报文丢包，从而导致RDMA数据网络报文重传，正确配置相关环境变量后，该问题解决。
**父主题：**[通信重传](toolsample6_039.html)