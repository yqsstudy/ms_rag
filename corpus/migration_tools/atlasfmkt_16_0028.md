---
title: "对于报错“No supported Ops kernel and engine are found for [ReduceStdV2A], optype [ReduceStdV2A]”，算子ReduceStdV2A不支持的问题"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0028.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0028.html"
---

# 对于报错“No supported Ops kernel and engine are found for [ReduceStdV2A], optype [ReduceStdV2A]”，算子ReduceStdV2A不支持的问题

可以通过用std求标准差再平方得到var，均值单独调用mean接口求来规避问题例如：



具体到代码中修改：

![](figure/zh-cn_image_0000002534398171.png "点击放大")
**父主题：**[FAQ](atlasfmkt_16_0024.html)