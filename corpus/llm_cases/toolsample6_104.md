---
title: "升级CANN版本"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_104.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_104.html"
---

# 升级CANN版本

CANN版本每一次升级都会优化部分算子。如果发现部分算子的执行性能差，或者执行在AI CPU上，考虑升级CANN版本。需要注意toolkit和kernel都要升级。通常情况下，升级CANN版本不会带来负面影响。

下面通过GridSampler2D算子的两个案例来直观感受解决方案，如图1所示，该算子在AI CPU上执行，性能较差；如图2所示，该算子虽然在vector_core上，但是执行效率也极低，这个案例的CANN版本比较旧。
**图1**
算子在AI CPU上执行**图2**
算子在vector_core上执行
针对以上两个问题，可以判断出在当前的CANN版本中，该算子在AI CPU上，存在性能问题，解决方案为将版本升级至CANN 8.0.RC3及以上版本，升级后改善明显，GridSampler2D耗时几乎可忽略。
**父主题：**[优化方法](toolsample6_094.html)