---
title: "概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0040.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0040.html"
---

# 概述

精度比对工具本身只提供自有实现算子在昇腾AI处理器上的运算结果与业界标准算子的运算结果的差异比对功能，输出的比对结果需要用户自行分析并找出问题。对于用户来说，对结果的分析工作也是一大难点。本节提供专家系统工具为用户提供精度比对结果的分析功能，有效减少用户排查问题的时间。

当前支持的分析检测类型有：Float16溢出检测、输入不一致检测、整网一致性检测（整网一致性检测包括：问题节点检测、单点误差检测和一致性检测三个小点）。
**父主题：**[比对结果专家建议](atlasaccuracy_16_0039.html)