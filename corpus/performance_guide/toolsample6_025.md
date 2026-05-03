---
title: 服务化工具
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_025.html?framework=pytorch
date_collected: 2026-04-29
---

# 服务化工具

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_025.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_025.html?framework=pytorch)

# 服务化工具

本章节主要介绍服务化工具使用场景和定位思路，具体问题的定位请参考 [服务化性能调优定位案例](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_111.html?framework=pytorch)。

  1. 广泛性调优：通过预检工具（msprechecker）对系统、环境变量及配置文件等方面进行检查，识别可能影响服务化性能的潜在问题。
  2. 针对性地调优：通过调整当前需求的配置项（输入输出长度、并发数等）优化服务化的调度，有以下两种方法：
     1. 服务化专家建议工具（msservice_advisor）：此工具能够快速提升服务化的性能，但不足以进行精细化的调优。
     2. 服务化自动寻优工具（modelevalstate）：适用于有针对性地提升服务化性能，能够达到人工调优所能实现的最佳性能的 95%。但该方法耗时较长，需要持续搜索参数以接近最优解。
  3. 如果仍未达到预期，可以使用服务化调优工具（msServiceProfiler）进行深入分析，此工具适用于熟悉整个服务化运作方式的用户。



**表1** 服务化性能工具介绍工具名称 | 工具简介  
---|---  
[推理预检工具（msprechecker）](https://gitee.com/ascend/msit/tree/master/msprechecker) | 支持推理前、推理中和推理后的全流程检测。

  * 推理前，提供一键式预检功能，全面排查环境变量、系统内核、配置文件等可能导致服务部署失败或性能下降的问题。
  * 推理过程中，支持将环境相关的所有数据完整落盘。
  * 推理结束后，支持对落盘文件进行比对，帮助识别差异点，便于复现基线环境。

  
[服务化专家建议](https://gitee.com/ascend/msit/blob/master/msserviceprofiler/docs/服务化专家建议工具.md) | 根据当前的Benchmark输出结果及MindIE service的config.json配置，结合理论分析性能上限，提出提升首令牌生成时间（TFTT）和吞吐量（Throughput）等关键指标的优化建议。  
[服务化自动寻优](https://gitee.com/ascend/msit/blob/master/msserviceprofiler/docs/服务化自动寻优工具.md) | 提供 MindIE 服务化和 vLLM 服务化的参数自动优化功能。利用先进的检索算法，在参数空间中高效寻找最优解，实现自动化调优。该功能同时支持轻量化设计，部署快速便捷，确保搜索结果更加准确。  
[服务化调优工具（msServiceProfiler）](https://gitee.com/ascend/msit/blob/master/msserviceprofiler/docs/服务化自动寻优工具.md) | 提供推理服务化性能数据采集接口的解析和拆解能力。此接口专为服务化调优设计，能够采集关键流程的起止时间点，识别并记录关键函数调用、关键事件、服务化调度等信息，同时支持采集算子信息，助力快速定位性能问题。如果想了解更多请参见《[性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)》的“[msServiceProfiler服务化调优工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0027.html)”章节。  
  
**父主题：** [性能工具的使用](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_009.html?framework=pytorch)
