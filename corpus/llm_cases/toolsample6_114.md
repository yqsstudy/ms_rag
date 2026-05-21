---
title: "显存瓶颈分析案例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_114.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_114.html"
---

# 显存瓶颈分析案例

#### 问题现象

DeepSeek双机服务化推理时，实际Batchsize无法达到192。

#### 分析

1. 采集服务化性能数据。
2. 组到192 Batchsize时，随着Decode增加，Decode推理到185次时，可以看到KV Block即将用尽，剩余36（初始1747）；随后剩余的KV Block降低到0，Batchsize降为72，降低前最后的192 Batchsize推理到253长度。
**图1**
查看数据

3. 从实际的执行来看，Batchsize=150的情况下，可以执行到Decode接近1000。
**图2**
实际执行

4. 估算显存瓶颈下的并发上限，Profiling显示可用的KV Cache block数量是1747，默认配置下每个Block大小是128个Token，根据1024输入2048输出的上下文要求，平均上下文为1536，KV Cache平均可容纳1747/[(1024+2048)/2/128]≈145。
**图3**
Block数量

5. 调整服务化参数，export NPU_MEMORY_FRACTION=0.96，maxSeqLen降低到3K，达到最优效果。
**父主题：**[服务化性能调优定位案例](toolsample6_111.html)