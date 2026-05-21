---
title: "工具概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0006.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0006.html"
---

# 工具概述

算子设计工具（msKPP，MindStudio Kernel Performance Prediction）具有性能建模分析、调用msOpGen算子工程和基于Ascend C模板库进行自动调优的功能，具体介绍如下：

- [性能建模](atlasopdev_16_0151.html#ZH-CN_TOPIC_0000002536800447)：在算子开发前，可根据算子的数学逻辑作为输入、基于msKPP提供的接口，写出一个算子实现方案的算子表达式，获得该方案的算子性能建模结果。由于本身针对性能的预测不需要进行真实的计算，仅需要依据输入和输出的规模，给出对应算法的执行时间，故而，可以在秒级给出性能建模结果。
- [调用msOpGen算子工程](atlasopdev_16_0172.html#ZH-CN_TOPIC_0000002536920429)[：msKPP工具提供的mskpp.tiling_func](atlasopdev_16_0185.html#ZH-CN_TOPIC_0000002536920433)[和mskpp.get_kernel_from_binary](atlasopdev_16_0186.html#ZH-CN_TOPIC_0000002504880688)接口，可以直接调用msOpGen算子工程。
- [自动调优](atlasopdev_16_0153.html#ZH-CN_TOPIC_0000002505040506)：msKPP提供模板库Kernel下发代码生成、编译、运行的能力，同时提供Kernel内代码替换并自动调优的能力。
**父主题：**[算子设计（msKPP）](atlasopdev_16_0005.html)