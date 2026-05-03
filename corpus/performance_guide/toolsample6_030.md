---
title: MindIE推理调优
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_030.html?framework=pytorch
date_collected: 2026-04-29
---

# MindIE推理调优

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_030.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_030.html?framework=pytorch)

# 总体介绍

快慢卡的快卡和慢卡是相对概念，快卡是在集群中首先完成计算任务的卡，慢卡是在集群任务中较慢完成计算任务的卡。在集群中往往需要完成集合通信，若不同卡完成任务的时间不同，则容易造成快卡等待慢卡完成计算的情况，从而使整个集群的性能劣化。

快慢卡是一种现象，背后的原因多种多样。通用的定位思路是，使用定点精确分析法，比对快卡和慢卡在MindStudio Insight时间线（Timeline）页签上的差异，确认具体原因。

形成慢卡的常见原因包括负载不均衡、计算性能波动、Host侧下发性能波动、数据加载性能波动等原因。

本节主要内容如下：

  * [快慢卡定点精确分析法](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_032.html?framework=pytorch)：介绍了快慢卡分析的通用思路。
  * [快慢卡定位Timeline操作案例](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_034.html?framework=pytorch)：演示了如何利用MindStudio Insight的时间线（Timeline）页签定位快慢卡问题。
  * [快慢卡定位算子比对操作案例](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_035.html?framework=pytorch)：演示了如何利用算子比对功能定位计算快慢卡问题。
  * [快慢卡案例补充](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_036.html?framework=pytorch)：展示更多快慢卡典型案例。



**父主题：** [快慢卡问题定位方法](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_030.html?framework=pytorch)
