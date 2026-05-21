---
title: "服务化参数优化案例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_200.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_200.html"
---

# 服务化参数优化案例

#### 问题现象

Qwen3-32B 单机4卡服务化部署，用户使用场景中并发较小且请求缓慢达到（最大并发40，实际使用情况接近请求速率9.4），PD混部的默认服务化配置下测试输入长度128输出长度100的性能，平均非首Token时延 48ms，但非首Token时延请求级别P99分位数（TPOT SLO P99）为157ms，导致个别请求流式输出卡顿，无法满足用户非首Token时延50ms的时延要求。

#### 解决方案

1. 观察默认服务化配置下，性能测试的初步结果如图1所示，可以发现（1）默认的Prefill优先调度下，首Token时延远最大值也只有158ms，说明Prefill性能正常且未达到算力瓶颈（2）P75首Token时延小于50ms，说明大多数非首Token时延正常，说明实际Decode性能已符合预期（3）注意到非首Token的P90/P99/最大时延偏高，推测是因为请求缓慢达到，新请求的Prefill打断推理中请求的Decode，导致部分非首Token需等待新请求Prefill完成，非首Token时延激增。

**图1**
![](figure/zh-cn_image_0000002503927324.png "点击放大")性能测试初步结果

2. 在此场景下，可以开启SupportSelectBatch，通过设置prefillTimeMsPerReq和decodeTimeMsPerReq调整Prefill和Decode的优先级，使调度器允许在一定情况下Decode优先。此策略可以减少“新请求Prefill打断推理中请求的Decode“的情况，进而提高连续Decode的占比，降低非首Token时延，如图2所示；虽然此策略会导致部分请求Prefill等待，但此案例场景中模型Prefill性能已经足够好，即使首Token时延略有增加，仍可通过调整优先级参数，将首Token时延控制在用户可以接受的范围内。

**图2**
非首Token时延劣化现象原理示意图

3. 调整优先级参数，prefillTimeMsPerReq越高，decodeTimeMsPerReq越低，则Decode优先级越高，反之则Prefill优先级越高；设置supportSelectBatch为true，prefillTimeMsPerReq为1000，decodeTimeMsPerReq为1，性能测试结果如图3，此时首Token时延增加至1562ms，平均非首Token降低至31.7ms，P99非首Token时延降低至36ms，整体流式输出流畅，满足用户需求。

**图3**
![](figure/zh-cn_image_0000002535807113.png "点击放大")调优后性能测试结果

**父主题：**[服务化性能调优定位案例](toolsample6_111.html)