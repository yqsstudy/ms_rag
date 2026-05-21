---
title: "问题信息收集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_005.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_005.html"
---

# 问题信息收集

在定位问题之前，务必收集准确的问题信息，具体请参考表1。
**表1**问题信息收集模板
类别

主要信息

说明

基本信息

模型类型

了解模型结构（类Llama、类GPT、是否是MoE等）。

作业规模

卡数、机器数。

并行策略

具体并行参数配置。

框架和版本

- 明确CANN、MindSpore或PyTorch的版本。
- 需确认近期是否有版本变更，以确定问题出现在版本变更之前还是之后。

关键问题描述

问题场景
在模型训练或推理过程中，其表现未达到预期标准或竞品水平，或者出现了性能下降等异常情况。
- 性能不及预期，一般出现在模型迁移后，相较于竞品性能不及预期。
- 性能出现抖动，模型长稳训练过程中，随机或伴随特定事件出现性能波动。
- 集群线性度不足，集群规模扩大后，模型性能没有按照预期增长。
- 纯模型性能差，相同配置下纯模型性能异常，参考训练问题解决。
- 服务化调度调优。

当前性能指标

[明确当前性能问题的状况，计算性能指标的优先级排序请参考《PyTorch 训练模型迁移调优指南](https://www.hiascend.com/document/detail/zh/Pytorch/720/ptmoddevg/trainingmigrguide/PT_LMTMOG_0002.html)[》中的“性能概述 > 性能指标 > 性能指标介绍](https://www.hiascend.com/document/detail/zh/Pytorch/720/ptmoddevg/trainingmigrguide/performance_tuning_0006.html)”章节。

优化目标

性能优化的目标

明确优化目标及来源，例如是否基于竞品对比，还是通过线性度推算等。
说明：
[若优化中涉及增大batchsize等方法，尽量避免使用单step时间等指标进行衡量，需参考《PyTorch 训练模型迁移调优指南](https://www.hiascend.com/document/detail/zh/Pytorch/720/ptmoddevg/trainingmigrguide/PT_LMTMOG_0002.html)[》中的“性能概述 > 性能指标 > 性能指标介绍](https://www.hiascend.com/document/detail/zh/Pytorch/720/ptmoddevg/trainingmigrguide/performance_tuning_0006.html)”章节，选取合理指标替换。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[性能问题的定位流程](toolsample6_003.html)