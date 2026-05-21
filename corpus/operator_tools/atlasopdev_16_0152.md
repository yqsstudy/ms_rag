---
title: "原理概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0152.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0152.html"
---

# 原理概述

msKPP为了达到理论性能的目标，基于如下表1对实际处理器进行计算和搬运类指令的性能建模。
**表1**msKPP建模假设性能
性能假设

说明

内部存储（Local Memory）无限，但用户在生命周期内可用的内存是有限的。

这个假设意味着在实际处理器的建模过程中，不考虑内存容量的限制。这允许用户或开发者可以自由地分配和使用内存资源，而不用担心内存不足的问题。在实际应用中，虽然物理内存是有限的，但这个假设可以简化模型，使得可以专注于其他性能相关的因素。

以统计评估的指令能力代表理论性能。

这个假设认为通过对处理器执行指令的统计分析可以得到其理论上的性能表现，处理器在执行指令时的平均性能可以反映出其最高性能潜力。这个假设有助于在设计和优化过程中，通过统计模型预测来提升处理器的性能。

下发无瓶颈。

这个假设意味着在数据或指令下发到处理器执行单元的过程中，不会遇到任何瓶颈或限制。也就是说，数据传输和指令调度可以无缝进行，不会因为任何硬件或软件的限制而降低性能。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[性能建模](atlasopdev_16_0151.html)