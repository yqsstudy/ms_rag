---
title: 性能问题的定位流程
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_003.html?framework=pytorch
date_collected: 2026-04-29
---

# 性能问题的定位流程

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_003.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_003.html?framework=pytorch)

# 整体定位流程

性能优化总体思路围绕[性能优化方向](toolsample6_002.html#ZH-CN_TOPIC_0000002503927264__section2430171411177)展开，具体步骤如下。

![](images/toolsample6_003_note_3.0-zh-cn.png)

性能优化的前提是不造成精度劣化，特殊情况下，需要对齐精度劣化是否能接受。

  1. **问题明确：** 请参考[问题信息收集](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_005.html?framework=pytorch)章节，收集必要信息。
  2. **性能问题排查：** 排查思路请参见[排查思路介绍](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_006.html?framework=pytorch)。
  3. **实验验证：** 在进行多次实验时，应严格控制变量，确保除了改变的策略外，其他参数和数据保持一致。



**父主题：** [性能问题的定位流程](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_003.html?framework=pytorch)
