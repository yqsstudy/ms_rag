---
title: 下发优化案例
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_046.html?framework=pytorch
date_collected: 2026-04-29
---

# 下发优化案例

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_046.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_046.html?framework=pytorch)

# Profiling采集性能膨胀

在按照[模型调优性能采集工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_013.html?framework=pytorch)采集Profiling数据的过程中，若开启了较高的采集等级，或者配置了较多采集项，性能数据采集打点时，可能会对Host侧造成较大压力，导致采集的性能数据膨胀失真。Profiling采集级别设置为Level2时，会造成通信调度膨胀，具体可能表现为，通信算子Host侧下发被阻塞，出现大段Free时长。

**解决方法** ：适当降低采集等级，建议非必要不开启Level2。若一定要开启，需结合Level1数据对比分析，以排除性能膨胀对数据的干扰。

**父主题：** [通信问题优化方案](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_028.html?framework=pytorch)
