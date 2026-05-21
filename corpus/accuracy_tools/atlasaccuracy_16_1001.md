---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_1001.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_1001.html"
---

# 总体说明

[对于该场景需要排查比对结果说明](atlasaccuracy_16_0036.html#ZH-CN_TOPIC_0000002504183998)。

TensorFlow 1.15训练/在线推理场景需准备的比对数据文件如下表所示。
**表1**TensorFlow 1.x的比对数据文件要求
文件

说明

获取方式

TensorFlow原始训练网络npy文件

标杆数据

[准备GPU侧npy文件](atlasaccuracy_16_0006.html#ZH-CN_TOPIC_0000002504183986)

计算图文件（*.txt）

计算图文件

[准备NPU侧dump数据和计算图文件](atlasaccuracy_16_0007.html#ZH-CN_TOPIC_0000002504343824)

通过昇腾AI处理器运行生成的训练网络dump数据文件

待比对数据
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[GPU vs NPU（TensorFlow 1.15训练/在线推理）](atlasaccuracy_16_0005.html)