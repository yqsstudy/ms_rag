---
title: "算子性能劣化对比分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_118.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_118.html"
---

# 算子性能劣化对比分析

#### 算子级性能比对

msprof-analyze compare工具提供了算子级性能比对，结果在performance_comparison_result_{timestamp}.xlsx中“OperatorCompare”和“OperatorCompareStatistic”的sheet页，呈现了全面的Shape信息、下发的kernel、device耗时，以及内存占用情况。

1. 查看“OperatorCompareStatistic”页，给出了算子调用次数与Device上运行总耗时，按照"Diff Duration(ms)"或"Diff Ratio"字段逆向排序，找出耗时差距TOP的算子。
2. 在“OperatorCompare”页，搜索耗时差距TOP的算子，查看具体执行的kernel耗时，如图1所示，寻找可优化点。
**图1**
查看执行的kernel耗时

#### module级性能比对

compare工具也支持module级比对，帮助快速识别劣化的模块和算子，并定位至代码块。

1. 查看“ModuleCompareStatistic”页， 筛选“Operator Name”字段为[ TOTAL ]，将模块总体情况按照“Device Self Time(ms)”字段逆向排序，找出耗时差距TOP的模块。
2. 查看“ModuleCompare”页，查找耗时差距TOP模块下的劣化算子。
3. 通过调用栈找到对应的代码行，如图2所示。
**图2**
查找代码行

**父主题：**[版本升级性能劣化定位方法论](toolsample6_116.html)