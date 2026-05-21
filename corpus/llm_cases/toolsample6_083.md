---
title: "定位实操技巧"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_083.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_083.html"
---

# 定位实操技巧

1. 在大规模场景下，若以规定时间内完成训练任务为目标，可以先明确优化目标，计算定位的收益（需要对比为定位问题在生产集群上实验、采集所造成的时间损耗，与完成优化后带来的收益）。
2. 针对大规模集群问题定位，首先需要考虑将大规模问题在小规模集群、甚至是单机环境上进行复现，方便实验，从而减小对生产任务的影响。方式包括但不限于N分、单机测试、预检等方式。
3. 实践中初次采集一般采用L1不带堆栈。在大规模集群场景下若直接写共享存储，可能会导致采集膨胀过大。另外，如果未进行良好资源隔离，可能会影响集群中其他作业。因此可以考虑首先将Profiling写到本地，再通过脚本分批收集至共享存储。
4. 若条件允许，可以在模型执行训练时就启动动态性能数据采集功能。
**父主题：**[集群性能异常波动问题定位方法论](toolsample6_081.html)