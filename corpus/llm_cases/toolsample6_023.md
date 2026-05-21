---
title: "内存（Memory）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_023.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_023.html"
---

# 内存（Memory）

以内存折线图呈现整体内存趋势，可以框选放大折线图中峰值区域，精准定位到内存消耗大的进程或算子。针对内存申请、释放异常的算子，跳转至时间线（Timeline），定位至具体代码。

内存优化思路：尽量增大Batchsize，最大化利用NPU内存。观察内存趋势，消除尖刺，削峰填谷。

查看图1，可以看到NPU利用率不足，观察到存在内存尖刺。
**图1**
典型Case
通过内存尖刺的时间点，框选锁定尖刺时间区域内算子。在内存申请/释放详情中，按内存申请大小降序排列，根据内存申请排名第一的算子跳转至时间线，定位至具体代码。如图2所示。随后，根据代码位置，和模型开发人员沟通确认有无优化空间。
**图2**
跳转至时间线
内存（Memory）界面还支持两卡间的比对功能，详情请参见《MindStudio Insight工具用户指南》的使用说明章节。
**父主题：**[单卡性能分析](toolsample6_021.html)