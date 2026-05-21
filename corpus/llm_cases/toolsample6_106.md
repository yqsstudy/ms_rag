---
title: "整体思路"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_106.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_106.html"
---

# 整体思路

MindIE推理性能可以从纯模型和服务化两个角度进行优化。

首先确认当前纯模型的性能是否有调优空间：

1. 版本基线覆盖的场景，和版本基线的性能比较，检查配置。
2. 版本基线未覆盖，或检查配置后仍存在问题的场景，先进行相同输入输出的纯模型测试。
3. 如果纯模型测试结果未达到预期，进行纯模型性能调优；如果达到预期，则进行服务化性能调优。
4. 服务化调优时性能瓶颈定位思路如图1所示。
**图1**
**服务化性能瓶颈定位流程图

父主题：**[MindIE推理性能解决方案](toolsample6_105.html)