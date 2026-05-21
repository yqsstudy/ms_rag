---
title: "模型执行耗时优化案例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_113.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_113.html"
---

# 模型执行耗时优化案例

#### 问题现象

DeepSeek PD分离大规模专家并行方案场景下，模型性能显著劣化。

#### 解决方案

1. 使用msServiceProfiler采集D节点服务化性能数据。
2. 分析采集的性能数据，发现同一个D节点内的两台不同服务器，Decode阶段存在快慢卡现象。具体表现为来自两个服务器上的两张卡单个Decode执行时间分别为260ms和170ms，差距较大；一张卡的算子泳道出现很长的"MIX_AIC"字段，说明此时该卡在执行通算融合算子并且同步等待时间很长，可以认为此卡为快卡，另一张卡"MIX_AIC"较短，为慢卡。
**图1**
快卡性能数据截图**图2**
慢卡性能数据截图

3. 从CANN CPU侧泳道（图1、图2中折叠为灰色）可以看出，每张卡启动任务的时间有差异，导致forward的第一个通算融合算子（moedispatch）时间不同，可以观察到90ms+的同步等待；去除第一个moedispatch后，剩余140ms左右的计算时间，两张卡算子性能接近——结合以上两点可以断定快慢卡是模型下发而非算子下发的时间差异导致的。
4. 通过在D节点开启分布式调度特性（使能环境变量MINDIE_ENABLE_DP_DISTRIBUTED，推理解决方案25.0.RC1之后的大规模专家并行方案已默认开启）后，性能恢复正常。
**父主题：**[服务化性能调优定位案例](toolsample6_111.html)