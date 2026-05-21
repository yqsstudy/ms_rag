---
title: "简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0001.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0001.html"
---

# 简介

内存泄漏检测工具（msLeaks）是基于昇腾AI处理器的内存检测工具，用于模型训练与推理过程中的内存问题定位。msLeaks工具提供内存泄漏检测、内存对比、内存块监测、内存拆解和低效内存识别等功能，帮助用户高效定位问题，快速处理。

#### 功能特性

msLeaks工具目前已支持的功能如表1。
**表1**msLeaks工具功能特性
功能

使用场景及说明

内存泄漏分析

针对内存长时间未释放和内存泄漏等问题，需要进行内存分析时，msLeaks工具提供内存泄漏分析和Kernel Launch粒度的内存变化分析功能，进行告警定位与分析。

内存对比分析

当两个Step内存使用存在差异时，可能会导致内存使用过多，甚至出现OOM（Out of Memory，内存溢出）的问题，则需要使用msLeaks工具的内存对比分析功能来定位并分析问题。

内存块监测

对大模型场景中，当遇到内存踩踏定位困难时，msLeaks工具支持通过Python接口和命令行两种方式，在算子执行前后对指定的内存块进行监测。根据内存块数据的变化，快速确定算子间内存踩踏的范围或具体位置。

内存拆解

msLeaks工具提供内存拆解功能，支持对CANN层和Ascend Extension for PyTorch框架的内存使用情况进行拆解，输出模型权重、激活值、梯度，以及优化器等组件的内存占用情况。

低效内存识别

在训练推理模型过程中，可能会存在部分内存块申请后未立即使用，或使用完毕后未及时释放的低效情况。msLeaks工具可帮助识别这种低效内存的使用现象，从而优化训练推理模型。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 支持的框架

当前msLeaks工具支持下列框架的内存检测：

- Ascend Extension for PyTorch 7.0.0及之后版本
- MindSpore 2.7.0及之后版本
- CANN 8.2.RC1及之后版本的ATB算子