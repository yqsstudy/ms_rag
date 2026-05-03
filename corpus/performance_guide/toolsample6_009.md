---
title: 性能工具的使用
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_009.html?framework=pytorch
date_collected: 2026-04-29
---

# 性能工具的使用

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_009.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_009.html?framework=pytorch)

# 性能工具总体介绍

本章将系统介绍如何在训练和推理任务中高效利用调优工具链，实现从性能数据收集到问题定位的完整闭环流程。训练场景主要聚焦于模型调优，推理场景同时包括模型调优与服务化调优。本章节将重点围绕模型调优和服务化调优两个方面进行介绍。

**表1** 性能工具简介调优维度 | 调优步骤 | 使用工具 | 详细说明  
---|---|---|---  
模型调优 | 性能数据采集 | 按照使能方式可以分为msprof命令行采集和AI框架Profiler接口采集两大类。具体介绍请参见[模型调优性能采集工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_013.html?framework=pytorch)

  * AI框架Profiler接口采集
    * PyTorch场景：Ascend PyTorch Profiler
    * MindSpore场景：MindSpore Profiler
  * msprof命令行采集

说明： msprof命令行工具无AI框架层数据。 | 选择合适的性能数据采集工具，记录模型运行过程中必要的AI框架与昇腾软硬件数据。详细介绍请参见[模型调优性能采集工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_013.html?framework=pytorch)。 msprof命令行工具主要采集CANN层与NPU层性能数据，是其它采集接口的底座。 AI框架Profiler接口封装了msprof命令行工具，进一步增加了对AI框架层性能数据的采集与解析，是训练或在线推理场景中最常用的采集方式。AI框架Profiler接口按照功能特性，可进一步分为常规采集（即静态采集）、动态采集、在线监测三种模式。 此外，部分训练或推理套件会对AI框架Profiler接口进行进一步封装，可直接通过套件内接口调用，例如[MindSpeed-MM](https://gitee.com/ascend/MindSpeed-MM/tree/master/mindspeed_mm/tools#profiling采集工具)、[MindFormers](https://www.mindspore.cn/mindformers/docs/zh-CN/r1.3.2/perf_optimize/perf_optimize.html#profiler工具)等。  
性能数据分析 | 模型调优快速分析工具：

  * 集群分析（cluster_analyze）


  * 专家建议（advisor）
  * 性能拆解比对（compare）

详细介绍请参见[模型调优快速分析（msprof-analyze命令行工具）](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_014.html?framework=pytorch) | 初步快速分析，可使用msprof-analyze提供的一系列功能，其中：

  * cluster_analyze：集群场景下，如千卡、万卡等无法直接分析全部数据的场景，可通过此工具来提取集群迭代耗时和通信数据， 快速定位慢卡、慢节点以及慢链路问题。建议结合MindStudio Insight可视化工具的Summary（概览）与Communication（通信）页签使用，具体使用方法请参考MindStudio Insight的[集群性能分析](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_018.html?framework=pytorch)章节。
  * advisor：将常见问题的识别和优化建议工具化，快速定界、定位典型性能问题，或为下一步分析指明方向。
  * compare：通过对训练耗时和内存占用的比对分析，定位到具体劣化的算子/API，帮助用户提升性能调优的效率；支持比较GPU与NPU之间、NPU与NPU之间的单卡性能差异，更推荐在GPU迁移NPU性能劣化、性能抖动等有基线比对数据的场景使用。

  
模型调优深入分析工具，具体分析请参见[模型调优深入分析（MindStudio Insight）](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_015.html?framework=pytorch)。 | MindStudio Insight可视化工具能够将以图形化方式展示完整的Profiling数据，助力用户深入理解和准确定位问题根源。该工具采用Top-Down分析方法，即从宏观到微观、从整个集群到单一节点逐步深入。若要详细了解其使用策略和具体操作，请参考[模型调优深入分析（MindStudio Insight）](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_015.html?framework=pytorch)。  
服务化调优 说明： 仅推理场景涉及服务化调优，具体服务化调优工具的使用请参见[服务化工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_025.html?framework=pytorch)。 | 环境预检 | [预检工具（msprechecker）](https://gitee.com/ascend/msit/tree/master/msprechecker) | 属于广泛的性能调优范畴，来检查是否因系统、环境变量或配置文件等问题影响了服务的整体性能。  
快速分析 | 

  * 服务化专家建议工具（msservice_advisor）
  * 自动寻优工具（modelevalstate）

| 

  * 服务化专家建议工具适用于快速提升服务化性能的场景，但不支持细粒度调优。
  * 自动寻优工具适用于针对性提升服务性能，能够实现接近手工调优最佳性能的95%效果。

  
深入分析 | 服务化调优工具（msServiceProfiler） | 进行深入分析，适合具备丰富服务化运作经验的用户。  
  
**父主题：** [性能工具的使用](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_009.html?framework=pytorch)
