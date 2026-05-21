---
title: "案例二：集群AllReduce通信算子等待时间过长"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_038.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_038.html"
---

# 案例二：集群AllReduce通信算子等待时间过长

#### 问题描述

256p集群allreduce通信算子等待时间长，线性度不达标。

#### 问题分析

问题直接表现是dp通信域存在耗时较长notify wait，如图1所示。
**图1**
dp通信域timeline分析
在通信界面找到此通信域，可以看到存在一个很长的notify wait，Elapse Time（通信总时间）差距巨大，最快卡和最慢卡差距200ms+。
**图2**
通信时长分析
如图3所示，同时打开快卡0卡和慢卡208卡的时间线（Timeline）界面，发现慢卡208主要是慢在tp通信上。慢卡208卡在一次micro的计算中tp域通信耗时494ms，快卡0卡tp域通信耗时340ms，差距较大。快慢卡的tp域通信传输速度基本一致，主要还是等待时间造成的差距。
**图3**
快卡0卡和慢卡208卡的Timeline界面
进一步观察和208卡同一个tp域的各卡，发现其中214卡是拖累整个tp域的慢卡。即214卡从tp域拖累了208卡，而208卡沿着dp域进一步拖累了0卡，214卡为其中真正的根因慢卡。如图4所示，对比208卡和214卡的时间线（Timeline），可以看到214卡存在Host下发较慢的问题。
**图4**
208卡和214卡的Timeline
如图5所示，通过时间线（Timeline）的框选统计功能，对比208卡与214卡的负责下发的CANN侧接口，可以看到214卡的CANN侧接口耗时明显高于208卡。
**图5**
208卡与214卡CANN侧接口框选统计
#### 定位完成

[通过快慢卡时间线（Timeline）定点比对分析，可以初步确认快慢卡差异是慢卡（214卡）的Host侧下发瓶颈导致的。进一步解决Host侧下发瓶颈，可参考Host Bound问题定位及解决方法](toolsample6_052.html)中内容。
**父主题：**[快慢卡案例补充](toolsample6_036.html)