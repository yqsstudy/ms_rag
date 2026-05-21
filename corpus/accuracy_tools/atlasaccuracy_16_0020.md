---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0020.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0020.html"
---

# 总体说明

[对于该场景需要排查比对结果说明](atlasaccuracy_16_0036.html#ZH-CN_TOPIC_0000002504183998)。

ONNX场景仅支持非量化的精度比对。需准备的比对数据文件如下表所示。
**表1**非量化原始模型 vs 非量化离线模型的比对数据文件要求
文件

说明

获取方式

非量化原始模型的npy文件

标杆数据

[准备ONNX模型npy文件](atlasaccuracy_16_0021.html#ZH-CN_TOPIC_0000002536023771)

通过ATC转换离线模型文件生成的json文件

获取算子的映射关系

[准备全网层信息文件](atlasaccuracy_16_0022.html#ZH-CN_TOPIC_0000002536143805)

非量化离线模型在昇腾AI处理器上运行生成的dump数据文件

待比对数据

离线推理场景各框架获取NPU环境的dump数据方法一致，请参考：

[准备离线模型dump数据文件](atlasaccuracy_16_0028.html#ZH-CN_TOPIC_0000002504343834)
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[GPU vs NPU（ONNX离线推理）](atlasaccuracy_16_0019.html)