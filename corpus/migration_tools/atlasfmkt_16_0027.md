---
title: "Muls算子不支持int64"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0027.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0027.html"
---

# Muls算子不支持int64

![](figure/zh-cn_image_0000002502558334.png "点击放大")

如上图所示，将label_batch.npu()改成label_batch.int().npu()，即把当前报错行的变量类型改成int32，规避此类Muls算子不支持int64的问题。
**父主题：**[FAQ](atlasfmkt_16_0024.html)