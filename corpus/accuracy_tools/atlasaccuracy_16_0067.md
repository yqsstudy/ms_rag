---
title: "数据格式要求"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0067.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0067.html"
---

# 数据格式要求

compare_vector.py精度比对工具将在后续版本下线，当前版本推荐使用上文中的msaccucmp.py工具。

当前版本支持多种比对方式，因此，对dump、npy文件命名有以下明确要求，准备数据时需要遵循。
**表1**数据文件命名规则
数据类型

数据命名格式

非量化原始模型的dump数据(Caffe)

*{op_name}.{output_index}.{timestamp}*.pb

量化原始模型的dump数据(Caffe)

*{op_name}.{output_index}.{timestamp}*.quant

非量化离线模型在昇腾AI处理器上运行生成的dump数据

*{op_type}.{op_name}.{task_id}.{timestamp}*

量化离线模型在昇腾AI处理器上运行生成的dump数据

*{op_type}.{op_name}.{task_id}.{timestamp}*

非量化原始模型的dump数据(TensorFlow)

*{op_name}.{output_index}.{timestamp}*.pb

npy文件(Caffe或TensorFlow)

*{op_name}.{output_index}.{timestamp}*.npy
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

命名格式说明：op_type、op_name对应的名称需满足“A-Za-z0-9_-”正则表达式规则，timestamp为16位时间戳，output_index、task_id为0~9数字组成。
**父主题：**[比对数据准备](atlasaccuracy_16_0066.html)